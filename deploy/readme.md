This directory contains all scripts that need to be deployed on the grid

for i in $( ls ); do
	qsub -o $PWD/logs -e $PWD/logs $i
done