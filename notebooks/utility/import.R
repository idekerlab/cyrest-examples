library(RCy3)
library(RJSONIO)
library(httr)

# 
port.number <- 1234
base.url <- paste("http://localhost:", toString(port.number), "/v1", sep="")

# Overview : Import sif format data and output 
# param filename: 
# SIF format : 
#   geneA <relationship type> geneB
#   geneB <relationship type> geneC geneD geneE
# output format : matrix. each value's type is string
#    geneA <relationship type> geneB
#    geneB <relationship type> geneC
#    geneB <relationship type> geneD
#    geneB <relationship type> geneE
sifDataToMatrix <- function(filename){
  f<-file(filename,"r")
  result.vec = c()
  repeat{
    str=readLines(con=f,1)
    if(length(str) == 0){
      break
    }
    original.line.vec <- strsplit(str, " ")[[1]]
    for(i in 1:length(original.line.vec)){
      if(i == 1){
        target.node <- original.line.vec[i]
        result.vec <- c(result.vec, target.node)
      }else if(i == 2){
        relationship <- original.line.vec[i]
        result.vec <- c(result.vec, relationship)
      }else if(i == 3){
        result.vec <- c(result.vec, original.line.vec[i])
      }else{
        result.vec <- c(result.vec, c(target.node, relationship, original.line.vec[i]))
      }
    }
  }
  return(matrix(result.vec, ncol=3, byrow = TRUE))
}

# 
createFrom <- function(network.list){
  deleteAllWindows(CytoscapeConnection())
  network.url = paste(base.url, "networks", sep="/")
  res <- POST(url=paste(network.url, "?source=url", sep=""), body=toJSON(network.list), encode="json")
  network.suid = unname(fromJSON(rawToChar(res$content)))
  
  networks.cw = list()
  for(suid in network.suid){
    suid.url = paste(network.url, suid$networkSUID, sep="/")
    graph.obj = fromJSON(rawToChar(GET(suid.url)$content))
    networks.cw <- c(networks.cw, list(existing.CytoscapeWindow(graph.obj$data$shared_name)))
  }
  return(networks.cw)
}

#
toCytoscape <- function (igraphobj) {
  # Extract graph attributes
  graph_attr = graph.attributes(igraphobj)
  
  # Extract nodes
  node_count = length(V(igraphobj))
  if('name' %in% list.vertex.attributes(igraphobj)) {
    V(igraphobj)$id <- V(igraphobj)$name
  } else {
    V(igraphobj)$id <- as.character(c(1:node_count))
  }
  
  nodes <- V(igraphobj)
  v_attr = vertex.attributes(igraphobj)
  v_names = list.vertex.attributes(igraphobj)
  
  nds <- array(0, dim=c(node_count))
  for(i in 1:node_count) {
    if(i %% 1000 == 0) {
      print(i)
    }
    nds[[i]] = list(data = mapAttributes(v_names, v_attr, i))
  }
  
  edges <- get.edgelist(igraphobj)
  edge_count = ecount(igraphobj)
  e_attr <- edge.attributes(igraphobj)
  e_names = list.edge.attributes(igraphobj)
  
  attr_exists = FALSE
  e_names_len = 0
  if(identical(e_names, character(0)) == FALSE) {
    attr_exists = TRUE
    e_names_len = length(e_names)
  }
  e_names_len <- length(e_names)
  
  eds <- array(0, dim=c(edge_count))
  for(i in 1:edge_count) {
    st = list(source=toString(edges[i,1]), target=toString(edges[i,2]))
    
    # Extract attributes
    if(attr_exists) {
      eds[[i]] = list(data=c(st, mapAttributes(e_names, e_attr, i)))
    } else {
      eds[[i]] = list(data=st)
    }
    
    if(i %% 1000 == 0) {
      print(i)
    }
  }
  
  el = list(nodes=nds, edges=eds)
  
  x <- list(data = graph_attr, elements = el)
  print("Done.  To json Start...")
  return (toJSON(x))
}

mapAttributes <- function(attr.names, all.attr, i) {
  attr = list()
  cur.attr.names = attr.names
  attr.names.length = length(attr.names)
  
  for(j in 1:attr.names.length) {
    if(is.na(all.attr[[j]][i]) == FALSE) {
      #       attr[j] = all.attr[[j]][i]
      attr <- c(attr, all.attr[[j]][i])
    } else {
      cur.attr.names <- cur.attr.names[cur.attr.names != attr.names[j]]
    }
  }
  names(attr) = cur.attr.names
  return (attr)
}


send2cy <- function(cygraph, style.name, layout.name) {
  network.url = paste(base.url, "networks", sep="/")
  res <- POST(url=network.url, body=cygraph, encode="json")
  network.suid = unname(fromJSON(rawToChar(res$content)))
  print(network.suid)
  
  # Apply Visual Style
  apply.layout.url = paste(base.url, "apply/layouts", layout.name, toString(network.suid), sep="/")
  apply.style.url = paste(base.url, "apply/styles", style.name, toString(network.suid), sep="/")
  
  res <- GET(apply.layout.url)
  res <- GET(apply.style.url)
}

.BBSOverride <- function(host, port) {
  ret <- list()
  if ((Sys.getenv("RCYTOSCAPE3_PORT_OVERRIDE") != "") &&  (Sys.getenv("RCYTOSCAPE3_HOST_OVERRIDE") != "")) {
    host = Sys.getenv("RCYTOSCAPE3_HOST_OVERRIDE")
    port = as(Sys.getenv("RCYTOSCAPE3_PORT_OVERRIDE"),"integer")
  }
  if (.Platform$r_arch == "x64") {
    if ((Sys.getenv("RCYTOSCAPE3_PORT_OVERRIDE_64") != "") &&  (Sys.getenv("RCYTOSCAPE3_HOST_OVERRIDE_64") != "")) {
      host = Sys.getenv("RCYTOSCAPE3_HOST_OVERRIDE_64")
      port = as(Sys.getenv("RCYTOSCAPE3_PORT_OVERRIDE_64"),"integer")
    }
  }
  #cat(paste("Using host", host, "and port", port, "."))
  
  ret["host"] <- host
  ret["port"] <- port
  ret
}


check.cytoscape.plugin.version = function(cyCon) 
{
  plugin.version.string = pluginVersion(cyCon)
  string.tmp1 = strsplit(plugin.version.string, ' ')[[1]][1]
  string.tmp2 = gsub('[a-z]', '', string.tmp1)
  string.tmp3 = gsub('[A-Z]', '', string.tmp2)
  plugin.version = as.numeric(string.tmp3)
  
  expected.version = 1
  
  if(plugin.version < expected.version) { 
    write(' ', stderr())
    write(sprintf('This version of the RCy3 package requires CyREST plugin version %s or greater.', expected.version), 
          stderr ())
    write(sprintf('However, you are using version %s. You must upgrade.', plugin.version), stderr ())
    write('Please visit the plugins page at http://www.cytoscape.org.', stderr ())
    write(' ', stderr())
    stop('Wrong CyREST version.')
  }
} # END check.cy

existing.CytoscapeWindow = 
  function(title, host='localhost', port=1234, copy.graph.from.cytoscape.to.R=FALSE) 
  {
    res <- .BBSOverride(host, port)
    host <- res$host
    port <- res$port
    
    uri <- sprintf('http://%s:%s', host, port)
    
    # establish a connection to Cytoscape
    cy.conn <- CytoscapeConnection(host, port)
    
    if (is.null(cy.conn)) {
      write(sprintf("ERROR in existing.CytoscapeWindow():\n\t Cytoscape connection could not be established >> NULL returned"), stderr())
      
      return()
    }
    # ensure the script is using the latest cyREST plugin version 
    check.cytoscape.plugin.version(cy.conn)
    
    existing.window.id = as.character(getWindowID(cy.conn, title))
    
    # inform user if the window does not exist
    if (is.na(existing.window.id)) {
      write(sprintf("ERROR in RCy3::existing.CytoscapeWindow():\n\t no window named '%s' exists in Cytoscape >> choose from the following titles: ", title), stderr())
      write(as.character(getWindowList(cy.conn)), stderr())
      return(NA)
    }
    
    # get graph from Cytoscape
    cy.window <- new('CytoscapeWindowClass', title=title, window.id=existing.window.id, uri=uri)
    
    if (copy.graph.from.cytoscape.to.R) {
      # copy over graph
      g.cy <- getGraphFromCyWindow(cy.window, title)
      cy.window <- setGraph(cy.window, g.cy)
      
      # copy over obj@suid.name.dict
      resource.uri <- paste(cy.window@uri, pluginVersion(cy.window), "networks", as.character(cy.window@window.id), sep="/")
      request.res <- GET(url=resource.uri)
      request.res <- fromJSON(rawToChar(request.res$content))
      
      if (length(request.res$elements$nodes) != 0){
        cy.window@suid.name.dict = lapply(request.res$elements$nodes, function(n) { 
          list(name=n$data$name, SUID=n$data$SUID) })
      }
      if (length(request.res$elements$edges) != 0){
        cy.window@edge.suid.name.dict = lapply(request.res$elements$edges, function(e) {
          list(name=e$data$name, SUID=e$data$SUID) })
      }
    }
    return (cy.window)
  }
## END e