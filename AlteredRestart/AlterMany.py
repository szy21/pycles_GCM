import AlteredRestart
import glob 
import os 
import netCDF4 as nc 
import subprocess 

def main():
        
    ars = {} 
    ars['output_root'] = '/cluster/scratch/presselk/altered_restart/'
    ars['restart_root'] = '/cluster/scratch/presselk/2dcrm/refac/rk3_s_subs_new/'
    ars['restart_time'] = '8553600'
    
    file = '/cluster/scratch/presselk/forcing/new_1.00x_default.nc'
    rt_grp = nc.Dataset(file, 'r')
    lons = rt_grp['lons'][:]
    rt_grp.close() 
     
    ars['case_list'] = list(lons)[-14:] 
    
            
    make_paths(ars) 
    get_restarts(ars)
    
    
    for case in ars['case_list']: 
        out_path = ars['case_paths'][case]
        restart_path = ars['case_restarts'][case] 
        
        print case, out_path, restart_path 
        restart_dbase = AlteredRestart.parse_files(restart_path, out_path)
        AlteredRestart.build_scratch_files(out_path, restart_dbase, quad=False)
 
    return 

def make_paths(ars):

    #Generate Altered Restarts 
    if not os.path.exists(ars['output_root']):
        os.mkdir(ars['output_root'])


    ars['case_paths'] = {}     
    #Now create the paths for each of the individual cases 
    for case in ars['case_list']:
    
        path = os.path.join(ars['output_root'], str(case))
        ars['case_paths'][case] = path 
        if not os.path.exists(path):
            os.mkdir(path) 
    
    return
    
def get_restarts(ars): 

    sim_dirs = glob.glob(os.path.join(ars['restart_root'], 'Output*')) 
    
    ars['case_restarts'] = {} 
    for case in ars['case_list']: 
        for sim in sim_dirs: 
            if str(case) in sim: 
                ars['case_restarts'][case] = os.path.join(os.path.join(sim, 'Restart'), ars['restart_time'])
                
                

    return  


if __name__ == '__main__': 
    main() 

