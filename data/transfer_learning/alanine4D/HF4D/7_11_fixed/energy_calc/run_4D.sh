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

v2_copy1=52.01
v2_copy=`echo ${v2_copy1} | sed -e 's/[eE]+*/\\*10\\^/'`
v2=`echo "scale=10; $v2_copy/1" | bc -l`

v3_copy1=60.4
v3_copy=`echo ${v3_copy1} | sed -e 's/[eE]+*/\\*10\\^/'`
v3=`echo "scale=10; $v3_copy/1" | bc -l`

v4_copy1=`awk 'NR==2' $infile`
v4_copy=`echo ${v4_copy1} | sed -e 's/[eE]+*/\\*10\\^/'`
v4=`echo "scale=10; $v4_copy/1" | bc -l`

# here we assign the variables
d4=$v1
d7=$v2
d11=$v3
d13=$v4

# computing all dependant angles
d5=`scale=0;echo "$d4+120" | bc -l`
d8=`scale=0;echo "$d7+120" | bc -l`
d9=`scale=0;echo "$d7+240" | bc -l`
d12=`scale=0;echo "$d11-180" | bc -l`

# writing values to Z-matrix
echo "d4 = " $d4 >> acq.gzmat
echo "d5 = " $d5 >> acq.gzmat
echo "d7 = " $d7 >> acq.gzmat
echo "d8 = " $d8 >> acq.gzmat
echo "d9 = " $d9 >> acq.gzmat
echo "d11 = " $d11 >> acq.gzmat
echo "d12 = " $d12 >> acq.gzmat
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
name=${v1}_${v2}_${v3}_${v4}
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

