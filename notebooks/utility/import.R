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


