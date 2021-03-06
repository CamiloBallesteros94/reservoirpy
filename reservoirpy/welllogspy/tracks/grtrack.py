import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

def grtrack(df: pd.DataFrame,
                gr: str = None,
                sp: str = None,
                lims: list = None,
                gr_max: int = 150,
                fm: pd.DataFrame = None,
                perf: pd.DataFrame = None,
                gr_sand_shale: pd.DataFrame = None,
                correlation: pd.DataFrame = None,
                fontsize: int = 8,
                dtick: bool = True,
                sand_flag: pd.Series=None,
                grid_numbers : list = [11,51],
                steps: list  = None,
                legend = False,
                gr_kw={},
                sp_kw={},
                fm_kw={},
                perf_kw={},
                gr_sand_kw={},
                gr_shale_kw={},
                corr_kw={},
                ax=None
               ):
    
    """
    Description:
        Function that plots in a defined Axes the Gammaray and Sp log.
    
    Parameters:
        depth: DataFrame that contains the depth 
        gr: str that contains the GammaRay values
        sp: str that contains the SP values
        lims: list that contains the depth limits to plot. e.g lims = [5800,6500]
        gr_max: int set the maximum limit to GammaRay axis 150,
        fm: DataFrame that contains the top and base of interest zones to color and bound
            fm = pd.DataFrame({'top':[11810,11945],'base':[11850,12400]})
        perf: DataFrame that contains the top and base of perforations. Plot a series of horizontal lines in the interval depth
                perf = pd.DataFrame({'top':[11810,11845],'bottom':[11815,11850]})
        gr_sand_shale: DataFrame that contains the top and base of different Clean and shaly base lines. Plot a series of vertical lines in the interval depth
                gr_sand_shale = pd.DataFrame({'top':[11810,11845],'bottom':[11815,11850],'sand':[10,23],'shale':[100,120]})
        correlation: DataFrame that contains the depth to correlate. Plot a series of horizontal lines in the interval depth
                gr_sand_shale = pd.DataFrame({'depth':[11810,11845,12500]})
        fontsize: int Fontsize for the plot ticks
        dtick: bool If show the depth ticks. Default True
        grid_numbers : List indicates the number of the grids to show in the depth axis for mayor and minor. Default list = [11,51]
        steps: List indicates the step size of the grids to show in the depth axis for mayor and minor. If 'steps' is provided 'grid_numbers' is not used
        gr_kw: kwargs for GammaRay Curve. Default 
                                                'color': 'darkred',
                                                'linestyle':'-',
                                                'linewidth': 2
        sp_kw: kwargs for sp Curve. Default 
                                                'color': 'darkblue',
                                                'linestyle':'-',
                                                'linewidth': 1
        fm_kw: kwargs for formation. Default 
                                                'color': 'black',
                                                'linestyle':'-',
                                                'linewidth': 1
        perf_kw: kwargs for perf Curve. Default 
                                                'color': 'black',
                                                'linestyle':'-',
                                                'linewidth': 1
        gr_sand_kw: kwargs for Gr sand curve. Default 
                                                'color': 'gold',
                                                'linestyle':'-',
                                                'linewidth': 1
        gr_shale_kw: kwargs for Gr shale curve. Default 
                                                'color': 'gray',
                                                'linestyle':'-',
                                                'linewidth': 1,
        correlation_kw: kwargs for correlation curve. Default 
                                                'color': 'red',
                                                'linestyle':'--',
                                                'linewidth': 2
        ax: Axes object to plot 
                
    
    """
    #Create the Axex
    grax= ax or plt.gca()
    
    # Default kwargs for all Lines
    def_gr_kw = {
    'color': 'darkred',
    'linestyle':'-',
    'linewidth': 2
    }
    for (k,v) in def_gr_kw.items():
        if k not in gr_kw:
            gr_kw[k]=v

    def_sp_kw = {
    'color': 'darkblue',
    'linestyle':'-',
    'linewidth': 1
    }    
    for (k,v) in def_sp_kw.items():
        if k not in sp_kw:
            sp_kw[k]=v
    
    def_fm_kw = {
    'color': 'black',
    'linestyle':'-',
    'linewidth': 2
    }    
    for (k,v) in def_fm_kw.items():
        if k not in fm_kw:
            fm_kw[k]=v

    def_perf_kw = {
    'color': 'black',
    'linestyle':'-',
    'linewidth': 1
    }    
    for (k,v) in def_perf_kw.items():
        if k not in perf_kw:
            perf_kw[k]=v
    
    def_gr_sand_kw = {
    'color': 'gold',
    'linestyle':'-',
    'linewidth': 1
    }    
    for (k,v) in def_gr_sand_kw.items():
        if k not in gr_sand_kw:
            gr_sand_kw[k]=v

    def_gr_shale_kw = {
    'color': 'gray',
    'linestyle':'-',
    'linewidth': 1
    }    
    for (k,v) in def_gr_shale_kw.items():
        if k not in gr_shale_kw:
            gr_shale_kw[k]=v

    def_corr_kw = {
    'color': 'red',
    'linestyle':'--',
    'linewidth': 2
    }    
    for (k,v) in def_corr_kw.items():
        if k not in corr_kw:
            corr_kw[k]=v

 ## Plot the Main Curves      
    #If GammaRay Provided   
    if gr is not None:  
        grax.plot(df[gr],df.index,**gr_kw)   #Plotting
        
     #If sp provided   
    if sp is not None:
        spax=grax.twiny()
        spax.plot(df[sp],df.index,**sp_kw)   #Plotting
        spax.xaxis.set_label_position("bottom")
        spax.xaxis.tick_bottom()
        spax.set_xlabel('Sp')
        spax.set_xticks(np.linspace(df[sp][df[sp]>-999.25].min(),df[sp][df[sp]>-999.25].max(),4))
        spax.set_xlim([df[sp][df[sp]>-999.25].min(),df[sp][df[sp]>-999.25].max()])
        

        
    # Set The lims of depth    
    grax.set_xlim([0,gr_max])           
    if lims==None: #Depth Limits
        lims=[df.index.min(),df.index.max()]

    grax.set_ylim([lims[1],lims[0]])

    #Set the vertical grid spacing
    if steps is None:
        mayor_grid = np.linspace(lims[0],lims[1],grid_numbers[0])
        minor_grid = np.linspace(lims[0],lims[1],grid_numbers[1])
    else:
        mayor_grid = np.arange(lims[0],lims[1],steps[0])
        minor_grid = np.arange(lims[0],lims[1],steps[1])

    #Set Gridding and ticks
    grax.set_xlabel('GammaRay')
    grax.tick_params("both",labelsize=fontsize)
    grax.grid(True,linewidth=1.0)
    grax.grid(True,which='minor', linewidth=0.5)
    plt.setp(grax.get_yticklabels(),visible=True)
    grax.set_yticks(minor_grid,minor=True)
    grax.set_yticks(mayor_grid)
    if dtick==True:
        grax.set_yticklabels(mayor_grid)
    else:
        grax.set_yticklabels([])
    grax.set_xticks(np.linspace(0,gr_max,4))
    grax.xaxis.set_label_position("top")
    grax.xaxis.tick_top()
    
    #Add Formations tops and bottoms
    if fm is not None:
        fm_ann = fm_kw.pop('ann',False)
        for i in fm.iterrows():
            if i[1]['md_top'] < lims[0] or i[1]['md_top'] > lims[1]:
                continue
            grax.hlines([i[1]['md_top']],0,gr_max, **fm_kw)
            if fm_ann:
               grax.annotate(f"Top of {i[1]['formation']}",xy=(gr_max-3,i[1]['md_top']-2),
                             xycoords='data',horizontalalignment='right',
                             bbox={'boxstyle':'round', 'fc':'0.8'})
                          

     #Add Interval Perforated
    if perf is not None:
        perf_ann = perf_kw.pop('ann',False)
        for i in perf.iterrows():
            if perf_ann:
                try:
                    grax.annotate(f"Top:{i[1]['md_top']} \nBottom:{i[1]['md_bottom']} \nNote:{i[1]['comment']}",
                                  xy=(0,(i[1]['md_top']+i[1]['md_bottom'])/2),xycoords='data',
                                  xytext=(-180, 0), textcoords='offset points',
                                  arrowprops=dict(arrowstyle="->"))
                except:
                    grax.annotate(f"Top:{i[1]['md_top']} \nBottom:{i[1]['md_bottom']}",
                    xy=(0,(i[1]['md_top']+i[1]['md_bottom'])/2),xycoords='data',
                    xytext=(-180, 0), textcoords='offset points',
                    arrowprops=dict(arrowstyle="->"))
                else: 
                    pass
        
            for j in np.arange(i[1]['md_top'],i[1]['md_bottom'],0.2):
                grax.hlines(j,0,15,**perf_kw)

    #Add Sand Gamma Ray line      
    if gr_sand_shale is not None:
        for i in gr_sand_shale.iterrows():
            try:
                grax.vlines(i[1]['gr_sand'],i[1]['md_top'],i[1]['md_bottom'],**gr_sand_kw)
            except:
                pass
            
            try:
                grax.vlines(i[1]['gr_shale'],i[1]['md_top'],i[1]['md_bottom'],**gr_shale_kw)
            except:
                pass
             
    #Add Correlation Line
    if correlation is not None:
        cor_ann = corr_kw.pop('ann',False)
        for i in correlation.iterrows():
            if i[1]['depth'] < lims[0] or i[1]['depth'] > lims[1]:
                continue
            grax.hlines(i[1]['depth'],0,gr_max, **corr_kw)
            if cor_ann:
                try:
                    grax.annotate(f"{i[1]['depth']} - {i[1]['comment']} ",xy=(gr_max-3,i[1]['depth']-1),
                                 xycoords='data',horizontalalignment='right',bbox={'boxstyle':'roundtooth', 'fc':'0.8'})
                except:
                    grax.annotate(f"{i[1]['depth']}",xy=(gr_max-3,i[1]['depth']-1),
                                 xycoords='data',horizontalalignment='right',
                                 bbox={'boxstyle':'roundtooth', 'fc':'0.8'})
                
    
    if legend:
        grax.legend() 