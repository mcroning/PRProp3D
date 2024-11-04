# PRProp3D
The software presented here is a three dimensional photorefractive beam propagation code. It is capable of modelling both static and dynamic interactions. It is inspired by results from the early 1990's in which beam propagation methods were used by several researchers including Alex Zozulya, Mordechai Segev and others. These were used to analyze several types of photorefractive phenomena in two dimensions: one transverse and one longitudinal.  With the advent of GPUs 3D time dependent calculations have become possible. The main program is PRcoupler.ipynb.  The files with 'video' in the name are for time dependent cases that require large amounts of storage.
The menu items are shown below.

<img width="560" alt="PRRrop3D GUI" src="https://github.com/user-attachments/assets/8ba39b23-a1e7-4996-be78-fa55596eb51b">

The program calculates unidirectional nonlinear optical beam propagation in three dimensions using photorefractive optical nonlinearities. It is based on the well-known split step beam propagation method which divides the process into a series of alternating steps along the longitudinal z direction. Diffractive propagation steps are handled using the angular spectrum of plane waves method[1] in which the angular spectrum of the optical field is calculated using the Fast Fourier Transform (FFT). The field is propagated as a set of individual plane waves for a short distance dz and the inverse Fourier transform is taken. The accumulated nonlinearity is then calculated from the intensity and applied as a spatially varying transparency. The process is repeated until the end of the interaction region is reached. The parameters used in the code are shown below, listed in the order that they appear in the input form.
The program with its default parameters will work on Google COLAB’s free accounts using its T4 GPU.  
The defaults are two beam coupling of 100 $\mu m$ diameter beams with input angles of $\theta$ = 0.1 radians and $\gamma \ell$ =-3. This results in the amplifaction of the beam labelled "Beam 1" by a factor of about 1.5. The longitudinal step size is 20 $\mu m$ and the crystal aperture is 1mm x 1mm. The interaction length is 4mm. A steady state calculation takes about 8 seconds. Time dependent beam coupling over 120 time steps to an end time of ten time units takes about 15 minutes. The program has also been tested with plane wave coupling with $\gamma \ell$ =-3, beam ratio 1 and fanning with $\gamma \ell$ = 10 and beam ratio zero.

Open on COLAB at the following link:
(https://colab.research.google.com/github/mcroning/PRProp3D/blob/main/PRcoupler.ipynb)

**Dependencies**

numpy, 
cupy, 
cupyx, 
scipy, 
matplotlib, 
PIL, ipywidgets, json, pathlib, tqdm, Ipython

**Instructions for use:**

**First Run**

In the notebook run the first three cells 1) to load modules and 2) load functions and 3) load sample images and set functions. 

For the first run answer n to the prompt for loading existing parameters. The default parameters are automatically loaded.

Run the initialization cell, then the calculation loop. On a COLAB T4 GPU, the first run will take about 10 seconds.

Run the postprocessing and display cell. This will show the input and output beams. The color scale can be interactively controlled by the sliders. In each case, the sum of the peak intensities of the input gaussian beams is normalized to unity. Also provided is a cross section of the input and output beams. Their vertical scales can be controlled by sliders. Next the far field is displayed in terms of direction cosines. These can be interpreted as $sin(\theta)\lambda/n$ where $\theta$ is the propagation angle, $\lambda$ is the opticalwavelength and $n$ is the refractive index of the medium in which the beam is traveling. The white circle arcs with radius of curvature one are the boundaries for the maximum direction cosine in the xy plane.
Finally for this first run you will see xz cross sections of the beam intensity and protorefractive grating field. Their color scales can also be adjusted with sliders. The next two cells are for generating movies of time dependent results and saving image and movie output as well as a json file of the parameters that were used.

**Subsequent Runs**
In the same session you can rerun the program with different parameters by updating the entries in the widgets. You do need to run the "Initialize parameters" cell each time you change parameters because the variables need to be explicitly updated. Subsequent runs of this initialization cell are faster.

**Time Dependent Model Runs**
By setting the time behavior dropdown to "Time Dependent" you can make temporal calculations of two beam coupling.
After running the postprocessing and display cell and using the sliders to adjust the output levels, run the Generate movies cell. Depending on the complexity of the fields, the time integration may become unstable.  If this happens the calculation cell will be aborted snd a notice given at the output of the cell. The output up to the failure can still be viewed and saved. In high resolution cases involving long runs it is recommended to separate movie generation from the beam propagation by using the program versions PRcoupler_large_videos.ipynb in a GPU COLAB instance then video_writer.ipynb which can be run separately in a CPU COLAB instance. This is because COLAB will sometimes disconnect if it senses that the GPU is not being used for part of the program.

**Saving Data** 
If you have checked the save data checkbox you may be prompted to allow access to your Google Drive. Running the save data cell will save a json file of the dictionary containing the parameters you used, formatted so it can be viewed by humans as a text file. Some output images will also be saved. These results are placed in a Google Drive folder whose name is specified in the Google Drive folder text box. 
In subsequent runs if you answer yes to the offer to load an existing parameter file, you may be asked to authorize Google Drive access. It is easest to use the file menu on the left side of the notebook to open the folder with your data and right click on the json or npz file then copy the path to the text box which will pop up. Data were saved in compressed npz files in earlier versions, but now the dictionary is saved as a readable json.

Some examples to try initially:
1) Run with default parameters.  Theis will show steady state two beam coupling of two 100 $\mu m$ waist beams with $\gamma \ell$ =-3. On a T4 this takes about 7 seconds. Input gain (coupling constant) and caculated gain are immediately reported below the calculation cell.  The calculated gain is from the standard two beam coupling formula: half the logarithm of the ratio of the output to input beam ratios.
2) Run the same in time dependent mode. Toggle the time behavior dropdown. Chenge the beam ratio to 6 to get a more pronounced amplification. This will take about 15 minutes for 120 time steps. You do not need to run the "Load samples..." cell again. The parameters are automatically updated. You do need to run the subsequent cells. The postprocessing and display cell will give the same outputs as in the static case, plus a graph of the output power of the amplified bema (Beam 1) vs time normalized to the characteristic photorefractive time constant.  The title of the graph includes the input coupling constant, and the coupling constant and time constant from a fit to a simple exponential growth to steady state model. Run the "Generate movies.." cell to make animations of the xz beam cross section and the output image.
3) Amplify an image. Use the image on beam dropdown to select 'Beam 1'. Select one of the MNIST images, or an AF resolution target. If you choose an MNIST image, I recommend checking the time dependence ofinvert image check box. If you want to see the amplified beam seclect "backpropagate output image". This is equivalent to bringing the amplified image bearing beam to an image plane.
4) Time dependent image amplification. When amplifying a real image, the phases in the interference pattern change slowly in the transverse direction and the time integration will be stable with long time steps ($t_0$ / 12), but the pattern becomes more complex for a phase image and shorter conservative time steps must be generally used to obtain stability. 
5) Model fanning. Set the gain to 10, beam ratio zero, noise type 'volume xy', check 'fanning study'. Without an image applied you should find that the fanning efficiency (ratio of power in fanning to input power) is about 33%.  You will see some minor dark ring artifacts. These are due to the large value of the longitidinal step size (20 $\mu m$). The white circle with radius one is the boundary for the maximum direction cosine in the xy plane.

![fanning_ss](https://github.com/user-attachments/assets/2c0949ad-5d47-41f2-8b9d-92dad17fdb6c)

6) Repeat the fanning modeling but with beam 1 waist 200 $\mu m$. You will see that the fanning is stronger than with the 100 $\mu m$ waist beam, and artifacts are beginning to creep in. The plot of the transverse grating shows that the fields have begun to wrap around and the far field image shows the characteristic fine dark artifact rings and the more diffuse rings at higher transverse wavenumbers.  These diffuse rings steal light from the true fanning and cause its intensity to be underestimated. The sharp diagonal features are due to wraparoud in the y direction. Note also that the fanning is truncated in the y direction.

![fanning_ss_200um](https://github.com/user-attachments/assets/e36fdbc5-314b-4988-918d-05e50028afdc)


By increasing the number of y samples , ysamp from 512 to 4096 we can lessen the wraparound artifacts in the y direction. This increases the computation time to 63 seconds

![fanning_ss_200um_4096x4096](https://github.com/user-attachments/assets/97a624bf-857e-4e78-b240-e8bfa2b35288)


Now it is just the z step related artifacts that remain. These can be decreased by reducing the longitudinal step size from 20 $\mu m$ to 5 $\mu m$ at
the cost of increasing the computation time to 270 seconds.The fanning efficiency is now 81%

![fanning_ss_200um_4096x4096_dz_5](https://github.com/user-attachments/assets/57218740-1ec7-45bd-bce6-0c7e9e59bc12)

**Explanation of parameters**

_gain length product_: The standard interaction strength used in the plane wave photorefractive theory. It is the coupling constant $\gamma$ times the length $\ell$ of the interaction region. Beam 1 will be amplified if the gain length product is negative.

_intensity beam ratio_: The ratio of the peak intensity of beam 2 to beam 1. This corresponds to the parameter _r_ in the plane wave theory.

_image on beam_: A dropdown to specify whether an image is to be applied at the input to one or both beams. This is useful for examining the nonlinearity induced image distortions.

_image type_: Determines whether the image is applies as an amplitude or phase transparency.

_image size normalized by waist_: The ratio between the transverse extent of the image to the waist of beam 1.

_external image file_: The path to a user supplied image for application the input. If there is no file at the path specified, the image specified in the std image dropdown will be used if called for. You can upload an image to COLAB's temporary storage space, or to your Google Drive. Most image file types are supported.

_standard image_: This dropdown is used to specify which of eleven standard supplied images will be used. One example of an MNIST digit for each of the digits 0 through 9 is supplied, as well as a 1951 Air Force Resolution Chart.

_invert image_: A toggle to provide the option to invert the input image.  This is sometimes useful for avoiding sharp edges at the image boundary.

_noise type_:
- _none_: No noise
- _volume xy_: Scattering screens are placed at the end of each propagation step with the nonlinear phase transparency. The correlation length of these screens is given by sigma (see parameter sigma below). They are uncorrelated in the z direction.

_scattering correlation length_: The correlation length in micrometers of the Gaussian random phase screens used to model optical scattering in the crystal.

_volume noise parameter_: scattering amplitude parameter $\epsilon$ which is the number of scattering phase screens times mean square deviation of each phase screen.

_Kerr coefficient_: magnitude of any nonlinearity that is directly proportional to the local intensity such as those due to thermal effects. It is normalized to the step size.

_x aperture um_: The transverse extent in micrometers of the interaction region in the x direction.

_y aperture um_: The transverse extent in micrometers of the interaction region in the y direction.

_x samples_: Number of grid points in the x direction.

_y samples_: Number of grid points in the y direction.

_interaction length_: Length $\ell$ in micrometers of interaction region in _z_ direction. Normally, the two beams, beam 1 and beam 2 will interact in the xz plane (azimuth = zero, see below).

_z step um_: The longitudinal step size in micrometers. Proper modelling of the optical effects of fine (micrometer scale) refractive index variations often requires step sizes of 10 $\mu m$ or less. 

_wavelength um_: Optical wavelength in free space in micrometers.

_waist 1_: The input beams are generated using the standard gaussian beam formula. The waist of beam 1 at its focus is waist 1. Its focus is halfway along the interaction length. If the beam waist is entered as a negative number, plane wave incidence is assumed,  This can be used for cross checking results with the standard plane wave two beam coupling theory[2].

_waist 2_: The waist of beam 2.

_use plane wave space charge model if appropriate_: For use when modelling plane wave two beam coupling theory. Only available for two coupled plane waves  propagating in xz plane with symmetric incidence angles.

_beam 1 polar angle_: The polar angle of incidence of beam 1, $\theta_1$. The definition of the angles is shown in Fig. 14.

_beam 2 polar angle_: The polar angle of incidence of beam 2, $\theta_2$

_azimuth 1_: The azimuth of beam 1, $\phi_1$

_azimuth 2_: The azimuth of beam 1, $\phi_2$

_backpropagate output image_: This gives the option to backpropagate the output field to the input plane without nonlinearities to allow comparison of images before and after photorefractive image processing, for example amplification. Without backpropagation, regular diffractive effects appear which can obscure distortions due to the photorefractive effect. Backpropagation is equivalent to bringing the output to an image plane.

_time behavior_: Choosing “Static” invokes the time independent model where the partial derivatives with respect to time are set to zero.  Choosing “Time Dependent” invokes the full time dependent model and generates movies showing time dependence and a graph of the power in beam 1 as a function of time as it is amplified or deamplified via two beam coupling. Time dependent calculations place a significant load on memory, since the full three-dimensional space charge electric field has to be stored from one time step to the next.

_end-time_: The duration of the simulation in units of the characteristic time $t_0$ (see appendix A). The duration of the time steps is end-time/number of time steps.

_time steps_: the number of time steps taken by the model before completion.

_use conservative time steps_: Set the time step to one fourth of the minimum anticipated time constant, $1/(1+(k_g/k_0)^2)$

_number of batches_: The propagation can be split into several longitudinal batches so that the GPU only needs to store the part of the space charge fields required by the current batch.  The full three-dimensional space charge field is stored in the CPU.

_fanning study_: If selected, spatial frequencies corresponding to the input beam are masked out in the far field so that the amplified scattering can be displayed without saturation by the remnants of the input beam.

_save noise seeds_: If selected the sequence of noise seeds used by the random number generator producing the scattering phase screens is saved to disk so that the same distribution can be used for both static and time dependent calculations and their outputs properly compared. 

_use old seeds_: Use noise stored on disk for the current calculation. For example, if comparing static and time dependent fanning distributions. The static case might be run first, its noise seeds saved, then reused for a time dependent calculation. If no noise file is on disk, new noise seeds will be generated. The seeds for each run are stored in the run’s data file (usually data.npz stored in a run’s output folder stored on a Google drive. They are also stored in the prdata dictionary.

_Google drive save folder_: When save output is selected, contains the name of the folder on Google Drive where run parameters and output of the run are stored in compressed form in data.npz. If the folder does not exist it will be created.

_save output_: If selected the run’s data will be stored to disk. It can be retrieved by the notebook PR_reader or at the beginning of each run instance.

_relative dielectric constant_: This is the dielectric constant of the interaction crystal normalized by the permittivity of free space $epsilon _0$.

_mobile charge density_: This is the density of empty sites in the crystal when in the dark with no photorefractive grating. Its units are m<sup>-3</sup>. Typical values are of the order of 10<sup>22</sup> m<sup>-3</sup>. From Garrett et al[3]: 6.4 x 10<sup>22</sup> m<sup>-3</sup>, and from Feinberg et al[4]: 1.9 x 10<sup>22</sup> m<sup>-3</sup>. 

_temperature K_: Temperature in Kelvin.

_ordinary refractive index_: Typical ordinary refractive index for BaTiO<sub>3</sub> (data available from various sources)

_extraordinary refractive index_: Typical extraordinary refractive index for BaTiO<sub>3</sub> (data available from various sources)

_crystal axis angle wrt z_: Crystal axis angle with respect to longitudinal z.

_dark intensity_: Equivalent optical intensity accounting for thermally ionized carriers. This intensity accounts for dark decay of the gratings. Normalized to the sum of the average peak intensity I<sub>0</sub> of the beams. (See appendix A)

_Tukey window edge_: The edge parameter for the Tukey (cosine taper) window[5] used to enable absorbing boundaries of the propagation lattice in both real space and Fourier space

[1] J. W. Goodman, Introduction to Fourier optics (W.H. Freeman, Macmillan Learning, New York, 2017), Fourth edition. edn.

[2] N. V. Kukhtarev, V. B. Markov, S. G. Odulov, M. S. Soskin, and V. L. Vinetskii, Ferroelectrics **22**, 949 (1979)

[3] M. H. Garrett, J. Y. Chang, H. P. Jenssen, and C. Warde, Journal of the Optical Society of America B-Optical Physics **9**, 1407 (1992).

[4] J. Feinberg, D. Heiman, A. R. Tanguay, and R. W. Hellwarth, Journal of Applied Physics 51, 1297 (1980).

[5] F. J. Harris, Proceedings of the IEEE **66**, 51 (1978).

