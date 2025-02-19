from PRProp3D import *
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from PIL import Image, ImageChops
import subprocess
from scipy.ndimage import zoom, gaussian_filter
import torch

#if not Path("/sample_images").exists():
#  process = subprocess.run(['git clone https://github.com/mcroning/sample_images'],shell=True)

#image on beam options options=['No Image','Beam 1','Beam 2','Beams 1 & 2']\
#time_behavior options=["Static", "Time Dependent"]
# noisetype options=["none","volume xy"]
prdict={
'gl':-3,
'rat':6.67,
'image_on_beam':'Beam 1',
'image_type':'real image',
'image_size_factor':1,
'external_image':'',
'std_image':'MNIST 3',
'image_invert':False,
'noisetype':"none",
'sigma':0.4,
'eps':0.02,
'kt':0,
'xaper':1000,
'yaper':1000,
'xsamp':4096,
'ysamp':512,
'rlen':4000,
'dz':20,
'lm':0.633,
'w01':100,
'w02':100,
'thout1':0.16,
'thout2':-0.16,
'phi1':0,
'phi2':0,
'backpropagate':False,
'time_behavior':"Time Dependent",
'tend':1,
'tsteps':12,
'use_cons_tsteps':False,
'batchnum_spec':1,
'fanning_study':False,
'use_old_seeds':False,
'folder':'',
'savedata':False,
'epsr':2500,
'NT':6.4e22,
'T':293,
'refin':2.4,
'Id':0.01,
'windowedge':0.1,
'E_app':0,
'skip':4,
'arrin':[]
}

if  prdict['w01'] < 0 or prdict['w02'] < 0: #we are using plane waves, so force periodic conditions

  fc=prdict['xsamp']*prdict['lm']/2/prdict['xaper']
  prdict['thout1']=np.arcsin(fc/(2**round(np.log(fc/np.sin(abs(prdict['thout1'])))/np.log(2))))*np.sign(prdict['thout1'])
  prdict['thout2']=-prdict['thout1']
  prdict['windowedge']=0

image_in=np.ones((28,28),dtype=np.uint8)  #default image
#make room for single display of image to be placed on beam


if prdict['external_image'] !=  "":
  image_file_name=prdict['external_image']
else:
  if prdict['std_image']=="MNIST 0":
    image_file_name = "./sample_images/mnist0.png"
  elif prdict['std_image']=="MNIST 1":
    image_file_name = "./sample_images/mnist1.png"
  elif prdict['std_image']=="MNIST 2":
    image_file_name = "./sample_images/mnist2.png"
  elif prdict['std_image']=="MNIST 3":
    image_file_name = "./sample_images/mnist3.png"
  elif prdict['std_image']=="MNIST 4":
    image_file_name = "./sample_images/mnist4.png"
  elif prdict['std_image']=="MNIST 5":
    image_file_name = "./sample_images/mnist5.png"
  elif prdict['std_image']=="MNIST 6":
    image_file_name = "./sample_images/mnist6.png"
  elif prdict['std_image']=="MNIST 7":
    image_file_name = "./sample_images/mnist7.png"
  elif prdict['std_image']=="MNIST 8":
    image_file_name = "./sample_images/mnist8.png"
  elif prdict['std_image']=="MNIST 9":
    image_file_name = "./sample_images/mnist9.png"
  elif prdict['std_image']=="AF Res Chart":
    image_file_name = "./sample_images/AF Res Chart.png"

if prdict['image_on_beam'] == 'No Image':
  image_file_name=""
display_input_image=False
if (prdict['image_on_beam'] != 'No Image') and Path(image_file_name).exists(): #path.exists(image_file_os.name)
  display_input_image=True
  image_in = Image.open(image_file_name)
  if prdict['image_invert']:
    image_in=ImageChops.invert(image_in)
  image_in = np.asarray(image_in)

  if np.ndim(image_in)==3: #color image to greyscale
      image_in=image_in.mean(axis=2)

imsizex=np.shape(image_in)[0]  #find original x dimension of image
imsizey=np.shape(image_in)[1]  #find original y dimension
maxsize=max(imsizex,imsizey)   #find maximum side length, maxsizenormint
if maxsize % 2 !=0: # make sure sides are of even length
        maxsize +=1
offset_x=-(imsizex-maxsize)//2
offset_y=-(imsizey-maxsize)//2

image_in_sq=np.ones((maxsize,maxsize))*np.max(image_in)  # make square image matrix that will hold input omage
image_in_sq[:imsizex,:imsizey]=image_in #load potentiallly non square image ont quare image matrix
image_in_sq=np.roll(image_in_sq,offset_x,axis=0)
image_in_sq=np.roll(image_in_sq,offset_y,axis=1)
image_in=image_in_sq.astype(np.uint16) #

image_in = np.asarray(image_in)
if prdict['w01'] > 0:
# find zoom factor for image to place it on beam 1
  zoomsc=prdict['image_size_factor']*prdict['w01']*np.sqrt(1+prdict['lm']*prdict['rlen']/2/(np.pi*prdict['w01']**2*prdict['refin']))/maxsize
else:
# if plane wave, image size is half of x aperture
  zoomsc=prdict['image_size_factor']*prdict['xaper']/2/maxsize
#scale and normalize to unity
arrin=(zoom(np.rot90(image_in),(zoomsc*prdict['xsamp']/prdict['xaper'],zoomsc*prdict['ysamp']/prdict['yaper']),order=0))
arrin=arrin/np.max(arrin)


# Check if CUDA (GPU support) is available
if torch.cuda.is_available():
  arrin=cp.array(arrin)
else:
  arrin=np.array(arrin)


prdata=Dict2Class(prdict)
prdata.arrin=arrin

beam1=Beam(prdata,beam_no=1,w0=prdata.w01,th=prdata.thout1,phi=prdata.phi1)
beam2=Beam(prdata,beam_no=2,w0=prdata.w02,th=prdata.thout2,phi=prdata.phi2)
derived=Derived(prdata,beam1,beam2)
if prdict['time_behavior']=='Static':
  amp,amp0,output=propagate(prdata,derived,dn=[Nlo.dn_pr_f],outputs=['ampxz','dnxz'])
  print(output.gainout.gain)
  imoutp=np.rot90(abs(output.gainout.ampp)**2,k=3)
  imoutm=np.rot90(abs(output.gainout.ampm)**2,k=3)

  iminp=np.rot90(abs(output.gainout.amp0p)**2,k=3)
  iminm=np.rot90(abs(output.gainout.amp0m)**2,k=3)

  xaper=prdata.xaper
  yaper=prdata.yaper

  fig1,ax1 = plt.subplots(1,2)
  ax1[0].set_title('Beam 1 in')
  im=ax1[0].imshow(iminp,extent=[-xaper//2,xaper//2,-yaper//2,yaper//2])
  fig1.colorbar(im,ax=ax1[0],shrink=0.5)  
  ax1[1].set_title('Beam 2 in')            
  im=ax1[1].imshow(iminm,extent=[-xaper//2,xaper//2,-yaper//2,yaper//2]) 
  fig1.colorbar(im,ax=ax1[1],shrink=0.5)
  fig1.tight_layout()

  fig2,ax2 = plt.subplots(1,2)
  ax2[0].set_title('Beam 1 out')
  im=ax2[0].imshow(imoutp,extent=[-xaper//2,xaper//2,-yaper//2,yaper//2])
  fig1.colorbar(im,ax=ax2[0],shrink=0.5)  
  ax2[1].set_title('Beam 2 out')            
  im=ax2[1].imshow(imoutm,extent=[-xaper//2,xaper//2,-yaper//2,yaper//2]) 
  fig1.colorbar(im,ax=ax2[1],shrink=0.5)
  fig1.tight_layout()
 

  fig3,ax3 = plt.subplots()
  ax3.plot(derived.x,iminp[prdata.ysamp//2,:])
  ax3.plot(derived.x,iminm[prdata.ysamp//2,:])
  ax3.set_xlabel('transverse x microns')
  ax3.set_ylabel('normalized intensity')
  ax3.legend(['beam1', 'beam2'])
  ax3.set_ylim(0,1)
  ax3.set_title('input')

  fig4,ax4 = plt.subplots()
  ax4.plot(derived.x,imoutp[prdata.ysamp//2,:])
  ax4.plot(derived.x,imoutm[prdata.ysamp//2,:])
  ax4.set_xlabel('transverse x microns')
  ax4.set_ylabel('normalized intensity')
  ax4.legend(['beam 1', 'beam2'])
  ax4.set_title('output')
  
  plt.show()
else:
  amp,amp0,output=propagate_t(prdata,derived,dndt=Nlo.dndt_f,outputs=['ampxzt','dnxyt','ampxyt'])
  print(output.gainout.gain)
