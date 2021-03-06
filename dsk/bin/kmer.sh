#!/bin/bash

#Import Properties File
GENOME_DIRECTORY=$1
OUTPUT_DIRECTORY=$2

for file in ${GENOME_DIRECTORY}/*.fna; do
     fileName="$(basename -- $file)"
     specieName="${fileName%.*}"
     outputH5Name=${specieName}"_output"
     outputKmerSpecieName=${specieName}"_kmer_output" 		
     echo ${fileName} " Kmer Counting Started "		 		
     
     # Change max-memory and kmer-size parameters accordingly	
     ./dsk/bin/dsk -nb-cores 1 -max-memory 300 -file ${GENOME_DIRECTORY}/${fileName} -kmer-size 11 -out ${OUTPUT_DIRECTORY}/${outputH5Name}
     ./dsk/bin/dsk2ascii -file ${OUTPUT_DIRECTORY}/${outputH5Name} -out ${OUTPUT_DIRECTORY}/${outputKmerSpecieName}		  	
     echo ${fileName} " Kmer counting finished "
done
for file1 in ${OUTPUT_DIRECTORY}*.h5; do   
     echo ${file1} " Deleted "
     rm -f ${file1}	
done

exit 1