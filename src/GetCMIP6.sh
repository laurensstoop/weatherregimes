# In this file the GeoPotential Height (500hPa) from CMIP6 is downloaded
# Author: Laurens P. Stoop, UU/KNMI/TenneT

### General stuff
# Create a timestamp
timestamp() {
  date +"%Y-%m-%d_%H-%M-%S"
}

### Setting everything up
# Set the directories
dir_out="/media/DataFiles/CMIP6/" 



# Set the model runs/scenarios to get
#MODELS='MPI-ESM-1-2-HAM'
#MODELS='MIROC-ES2L'
#MODELS='CNRM-CM6-1'
#MODELS='CMCC-CM2-SR5'
#MODELS='CESM2-WACCM'
#MODELS='CESM2'
#MODELS='NorESM2-MM'
MODELS='IPSL-CM6A-LR'
#MODELS='CESM2-WACCM-FV2' # not complete set
#MODELS='UKESM1-0-LL'
#MODELS='HadGEM3-GC31-LL'
#MODELS='GFDL-ESM4'
#MODELS='CNRM-ESM2-1'
#MODELS='NorESM2-LM'
#MODELS='CMCC-ESM2'
#MODELS='MPI-ESM1-2-LR'
#MODELS='CESM2-FV2' # not complete set
#MODELS='EC-Earth3-Veg-LR'
#MODELS='CanESM5'

### This mega loop is required to correctly name the files
# Select the models
for M in $MODELS
do
    
    # Make the directory if it does not exist
    if [[ ! -e ${dir_out}${M} ]]; then
        mkdir -p ${dir_out}${M} 
    fi


    # Update the reader & copy to log
    echo "$(timestamp): GetCMIP6 data Model ${M} "


    # Get the data
    acccmip6 -o D -v zg500 -f day -m ${M} -e '['piControl','historical','ssp585','ssp126','ssp370']' -dir ${dir_out}${M}

done

