#!/bin/bash


exe=/projappl/project_2000382/share_BOSS/aims.171221_1.scalapack.mpi.x

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

# transform the xyz into coordinates for FHI-aims:
awk 'NR>2' acq.xyz > acq.coo
./xyz2geo.sh < acq.coo > geometry.in
rm *.coo

# create directory structure for each acquisition
name=${d4}_${d13}
echo $name
mkdir ./tmp_${name}
cp control.in geometry.in ./tmp_$name/
cd ./tmp_$name

# run static FHI-aims simulation
srun $exe < /dev/null > acq.stdout

# parse amber output file for total energy
E=($(grep "s.c.f. calculation " acq.stdout | tail -1 | awk '{print $12}'))
# MT: I usually use:
# Etot=`grep "caution " $name.stdout | tail -1 | awk '{print $11}'`

echo $E > ../$outfile
cd ../

# clean
rm acq.*

# return to original directory
cd $here

