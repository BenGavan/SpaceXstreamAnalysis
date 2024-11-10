from typing import List
import numpy as np
import matplotlib.pyplot as plt
import os


class DualXPlot:
    def __init__(self, xs: List[np.ndarray], ys: List[np.ndarray], xlabel: str, ylabel: str):
        if len(xs) != len(ys):
            raise Exception('len(xs) != len(ys) - need to have the same number of data sets')
        
        self.xs = xs
        self.ys = ys
        self.xlabel = xlabel
        self.ylabel = ylabel
        
    def plot(self, ax, x1_end=None, x2_end=None, y_start=None, y_end=None, notes='', x_offset:List[float]=None, title:str=None):
        xs = self.xs
        ys = self.ys.copy()

        if x_offset is not None and type(x_offset) is float:
            x_offset = [x_offset for _ in range(len(self.xs))]

        if x_offset is None:
            x_offset = [0 for _ in range(len(self.xs))]
        
        is_dual_x_axis = x2_end is not None
        
        if x1_end is None:
            x1_end = np.max(xs)
            
        if y_start is None:
            y_start = np.min(ys)
            
        if y_end is None:
            y_end = np.max(ys) * 1.1
            
        if is_dual_x_axis:
            ax1 = ax.twiny()
        
        for i in range(len(xs)):
            # get index of end of x1 region
            # TODO: Make more robust: if there is noise on x signal, the first index might not be when it crosses onto x2 axis.  Might be a good idea to split the data into to sets, {x1,y} and {x2, y}
            x1_end_index = None
            for j in range(len(xs[i])):
                if xs[i][j] > x1_end:
                    x1_end_index = j
                    break

            x = xs[i] + x_offset[i] * i
            y = ys[i]
               
            ax.scatter(x[:x1_end_index], y[:x1_end_index], marker='.', c='#000000', s=1)
            if is_dual_x_axis:
                ax1.scatter(x[x1_end_index:], y[x1_end_index:], marker='.', c='#000000', s=1)

        ax.set_xlim([0, x1_end])
        if is_dual_x_axis:
            ax1.set_xlim([x1_end, x2_end])
        
        ax.set_ylim([y_start, y_end])
        
        ax.grid(color='#6b6b6b', linewidth=0.3, alpha=0.3)
        
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.ylabel) 
        
        if title is None:
            title = f' ({notes})'  
            
        if title != '':
            ax.set_title(title)
                     

class MulitFigure:
    def __init__(self, xss: List[List[np.ndarray]], yss: List[List[np.ndarray]], xlabels: List[str]=None, ylabels: List[str]=None, titles:List[str]=''):  # Passing in n sets of data. Each set of data can have m series.  Each of the n sets of the data will be plotted on the n seperate axes.
        self.xss = xss
        self.yss = yss
        self.n_sets_data = len(self.xss)
        
        if type(xlabels) != list :
            xlabels = [xlabels for _ in range(self.n_sets_data)]
        self.xlabels = xlabels
        
        if type(ylabels) != list :
            ylabels = [ylabels for _ in range(self.n_sets_data)]
        self.ylabels = ylabels
        
        if type(titles) != List:
            titles = [titles for _ in range(self.n_sets_data)]
        self.titles = titles
        
    def plot(self, outpath: str, x1_end:List[float]=None, x2_end:List[float]=None, y_end:List[float]=None, x_offset:List[float]=None):        
        if x1_end is None:
            x1_end = [None for _ in range(self.n_sets_data)]
        
        if x2_end is None:
            x2_end = [None for _ in range(self.n_sets_data)]
        
        if y_end is None:
            y_end = [None for _ in range(self.n_sets_data)]
            
        if x_offset is None:
            x_offset = [None for _ in range(self.n_sets_data)]
        
        ncols = min(2, self.n_sets_data)  
        rows_per_page = min(5, int(np.ceil(self.n_sets_data/ncols)))
        
        n_rows = int(np.ceil(self.n_sets_data / ncols))
        pages = int(np.ceil(n_rows/rows_per_page))

        for page_index in range(pages):
            #nrows = min(rows_per_page, int(np.ceil(len(self.data) - ncols*rows_per_page*page_index)/ncols))
            nrows = rows_per_page  # will plot blank plots, but will keep plot scaling the same 
            fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(7*ncols, 5*nrows))
            
            n_plots_per_page = nrows * ncols
            index_offset = page_index * n_plots_per_page
            for i in range(index_offset, min(index_offset+n_plots_per_page, self.n_sets_data)):
                row_index = int((i-index_offset) / ncols)
                col_index = i % ncols
                
                print(f'plotting {i}')
                if nrows != 1 and ncols != 1:
                    a = ax[row_index, col_index]
                elif ncols != 1:
                    a = ax[col_index]
                elif nrows != 1:
                    a = ax[row_index]
                else:
                    a = ax
                    
                DualXPlot(self.xss[i], self.yss[i], self.xlabels[i], self.ylabels[i]).plot(a, x1_end=x1_end[i], x2_end=x2_end[i], y_end=y_end[i], x_offset=x_offset[i], title=self.titles[i])
        
            fig.tight_layout()
            outfilepath = os.path.join(outpath, f'{page_index}.png')
            print(f'saving plot to: {outfilepath}')
            fig.savefig(outfilepath, dpi=500)
            print(f'finished saving plot')
            plt.close(fig)
