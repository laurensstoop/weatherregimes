# define the storage location
file_in1='/media/DataGate2/ERA5/CF'
file_out='/media/stoop/ExtremePro2/ERA5/WR-CF'

for Y in $(seq 1979 2020);do  
    cdo mergetime $file_in1/ERA5_CF_${Y}01.nc $file_in1/ERA5_CF_${Y}02.nc $file_in1/ERA5_CF_${Y}03.nc $file_in1/ERA5_CF_${Y}12.nc $file_out/ERA5-EU_CF_DJFM_${Y}.nc
done
