#!/bin/bash
set -e

# go to calculation directory
here=$(pwd)
cd energy_calc

# input output files
infile="variables.in"
outfile="energy.out"

# copy original structure as z-matrix and modify it based on given variables
cp alanine.gzmat acq.gzmat

# this inelegant code loads the number, changes format and turns into bash floating point
v1_copy1=`awk 'NR==1' $infile`
v1_copy=`echo ${v1_copy1} | sed -e 's/[eE]+*/\\*10\\^/'`
v1=`echo "scale=10; $v1_copy/1" | bc -l`

v2_copy1=`awk 'NR==2' $infile`
v2_copy=`echo ${v2_copy1} | sed -e 's/[eE]+*/\\*10\\^/'`
v2=`echo "scale=10; $v2_copy/1" | bc -l`

# here we assign the variables
d4=$v1
d13=$v2
d5=`scale=0;echo "$d4+120" | bc -l`

echo "d4 = " $d4 >> acq.gzmat
echo "d5 = " $d5 >> acq.gzmat
echo "d13 = " $d13 >> acq.gzmat

# run babel run convert modified z-matrix file into xyz file
babel -igzmat acq.gzmat -oxyz acq.xyz &> .dump

# save the xyz structure
cat acq.xyz >> $here/movie.xyz

# transform the xyz into rst coordinates for amber using a python script
python3 xyz2rst.py acq.xyz acq.rst

# run static amber simulation using the rst coordinate file
srun sander -O -i md.in -o acq.out -c acq.rst -p system.prmtop

# parse amber output file for total energy
E=`grep Etot acq.out | awk '{print $3}'`
echo $E > $outfile

# save amber output file
cat acq.out >> $here/amber.out

# clean
rm -rf acq*
rm -rf mdinfo
rm -rf mdfrc
rm -rf restrt

# return to original directory
cd $here

