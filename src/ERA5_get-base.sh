# define the storage location
file_in1='/media/DataStager1/ERA5'
file_in2='/media/DataDrive/ERA5-EU_BASE'
file_out='/media/stoop/ExtremePro2/ERA5/WR-base'
var='mpsl' #ssrd t2m wspd100m mpsl wspd

for Y in $(seq 1979 2020);do  
    cdo selmon,1,2,3,12 $file_in2/ERA5-EU_${var}_${Y}.nc $file_out/ERA5-EU_${var}_DJFM_${Y}.nc
done
