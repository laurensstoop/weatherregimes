#!/usr/bin/bash

# """
# Created on Mon 24 Dec 2022 11:15
# 
# @author: Laurens Stoop - l.p.stoop@uu.nl
# """

for Y in $(seq 1979 2020);do  
    echo ${Y}
	cdo daymean /Volumes/ExtremePro2/ERA5/WR-base/ERA5-EU_mpsl_DJFM_${Y}.nc /Volumes/ExtremePro2/ERA5/WR-daily/ERA5-EU_mpsl_DJFM_${Y}_daily.nc
	cdo daymean /Volumes/ExtremePro2/ERA5/WR-base/ERA5-EU_ssrd_DJFM_${Y}.nc /Volumes/ExtremePro2/ERA5/WR-daily/ERA5-EU_ssrd_DJFM_${Y}_daily.nc
	cdo daymean /Volumes/ExtremePro2/ERA5/WR-base/ERA5-EU_t2m_DJFM_${Y}.nc /Volumes/ExtremePro2/ERA5/WR-daily/ERA5-EU_t2m_DJFM_${Y}_daily.nc
	cdo daymean /Volumes/ExtremePro2/ERA5/WR-base/ERA5-EU_wspd100m_DJFM_${Y}.nc /Volumes/ExtremePro2/ERA5/WR-daily/ERA5-EU_wspd100m_DJFM_${Y}_daily.nc
	cdo daymean /Volumes/ExtremePro2/ERA5/WR-CF/ERA5-EU_CF_DJFM_${Y}.nc /Volumes/ExtremePro2/ERA5/WR-daily/ERA5-EU_CF_DJFM_${Y}_daily.nc
	
done


