# PRProp3D
The software presented here is a three dimensional photorefractive beam propagation code. It is capable of modelling both static and dynamic interactions.
The menu items are shown below.

![image](https://github.com/user-attachments/assets/bb0ca750-cbe9-40f5-b944-09c42b79222e)

The program calculates unidirectional nonlinear optical beam propagation in three dimensions using photorefractive optical nonlinearities. It is based on the well-known split step beam propagation method which divides the process into a series of alternating steps along the longitudinal z direction. Diffractive propagation steps are handled using the angular spectrum of plane waves method[14] in which the angular spectrum of the optical field is calculated using the Fast Fourier Transform (FFT). The field is propagated as a set of individual plane waves for a short distance dz and the inverse Fourier transform is taken. The accumulated nonlinearity is then calculated from the intensity and applied as a spatially varying transparency. The process is repeated until the end of the interaction region is reached. The parameters used in the code are as follows, listed in the order that they appear in the input form.
The program with its default parameters will work on Google COLAB’s free accounts using its T4 GPU.  
The defaults are two beam coupling of 100 $\mu m$ diameter beams with input angles of $\theta$ = 0.1 radians and $\gamma \ell$ =-3. The longitudinal step size is 20 $\mu m$ and the crystal aperture is 1mm x 1mm. The interaction length is 4mm. A steady state calculation takes about 8 seconds. Time dependent image amplification over 80 steps to an end time of ten time units takes about 10 minutes. The program has also been tested with plane wave coupling with $\gamma \ell$ =-3, beam ratio 1 and fanning with $\gamma \ell$ = 10 and beam ratio zero.

Open on COLAB at the following link:
(https://colab.research.google.com/github/mcroning/PRProp3D/blob/main/PRcoupler.ipynb)
Instructions for use:
In the notebook run the first two cells 1) to load modules and 2) define functions and load sample images


Some examples to try initially:
1) Run with default parameters.  Theis will show steady state two beam coupling of two 100 $\mu m$ waist beams with $\gamma \ell$ =-3. On a T4 this takes about 7 seconds
2) Run the same in time dependent mode. Toggle the time behavior dropdown. Chenge the beam ratio to 6 to get a more pronounced amplification. This will take about ten minutes.
3) Amplify an image. Usse the image on beam dropdown to select 'Beam 1'. Select one of the MNIST images, or an AF resolution target. If yoou choose am MNIST image, I recommend to check the invert image check box. If you want to see the amplified beam seclect "backpropagate image". This is eqiovalent to bringing the amplified image bearing beam to an image plane. You might want to select static time dependence at first. When amplifying a real image, the phases in the interference pattern change slowly in the transverse direction and the time integration will be stable with long time steps ($t_0$ / 8), but the pattern becomes more complex for a phase image and shorter conservative time steps must be generally used to obtain stability.
4) Model fanning. Set the gain to 10, beam ratio zero, noise type 'volume xy', check 'fanning study'. Without an image applied you should find that the fanning efficiiency is about 33%
5) Repeat the fanning modeling but with beam 1 waist 200 $\mu m$. You will see that the fanning is stronger than with the 100 $\mu m$ waist beam, and artifacts are beginning to creep in. The plot of the transverse gration goild shows that the fields have begun to wrap around and the far field image shows the characteristic artifact rings
![image](https://github.com/user-attachments/assets/c995f44f-72b4-426d-a244-f21f4082d3cc)

By increasing the number of y samples , ysamp from 512 to 4096 we can lessen the wraparound artifacts in the y direction. This increases the computation time to 63 seconds

![image](https://github.com/user-attachments/assets/9e7cf421-2238-4a54-bd5f-02f3b7630168)

Now it is just the z step related artifacts that remain. These can be decreased by reducing the longitudinal step size from 20 $\mu m$ to 5 $\mu m$ at
the cost of increasing the computation time to 270 seconds

![image](https://github.com/user-attachments/assets/e10ed2ae-80ee-48c0-8baf-e71cd3a94e50)

**Explanation of parameters**

_gain length product_: The standard interaction strength used in the plane wave photorefractive theory. It is the coupling constant $\gamma$ times the length $\ell$ of the interaction region.

_intensity beam ratio_: The ratio of the peak intensity of beam 2 to beam 1. This corresponds to the parameter _r_ in the plane wave theory.

_image on beam_: A dropdown to specify whether an image is to be applied at the input to one or both beams. This is useful for examining the nonlinearity induced image distortions.

_image type_: Determines whether the image is applies as an amplitude or phase transparency.

_image size normalized by waist 1_: The ratio between the transverse extent of the image to the waist of beam 1.

_external image file_: The path to a user supplied image for application the input. If there is no file at the path specified, the image specified in the std image dropdown will be used if called for.

_standard image_: This dropdown is used to specify which of eleven standard supplied images will be used. One example of an MNIST digit for each of the digits 0 through 9 is supplied, as well as a 1951 Air Force Resolution Chart.

_invert image_: A toggle to provide the option to invert the input image.  This is sometimes useful for avoiding sharp edges at the image boundary.

_noise type_: 

- _none_: No noise
- _volume xy_: Scattering screens are placed at the end of each propagation step with the nonlinear phase transparency. The correlation length of these screens is given by sigma (see parameter sigma below). They are uncorrelated in the z direction.

_scattering correlation length_: The correlation length of the Gaussian random phase screens used to model optical scattering in the crystal.

_volume noise parameter_: scattering amplitude parameter $\epsilon$ which is the number of scattering phase screens times mean square deviation of each phase screen.

_Kerr coefficient_: magnitude of any nonlinearity that is directly proportional to the local intensity such as those due to thermal effects. It is normalized to the step size.

_x aperture um_: The transverse extent in micrometers of the interaction region in the x direction.

_y aperture um_: The transverse extent in micrometers of the interaction region in the y direction.

_x samples_: Number of grid points in the x direction.

_y samples_: Number of grid points in the y direction.

_interaction length_: Length $\ell$ in micrometers of interaction region in _z_ direction. Normally, the two beams, beam 1 and beam 2 will interact in the xz plane (azimuth zero, see below).

_z step um_: The longitudinal step size in micrometers. Proper modelling of the optical effects of fine (micrometer scale) refractive index variations often requires step sizes of 10 $\mu m$ or less. 

_wavelength um_: Optical wavelength in free space in micrometers.

_waist 1_: The input beams are generated using the standard gaussian beam formula. The waist of beam 1 at its focus is waist 1. Its focus is halfway along the interaction length. If the beam waist is entered as a negative number, plane wave incidence is assumed,  This can be used for cross checking results with the standard plane wave two beam coupling theory[^1].

_waist 2_: The waist of beam 2.

_use plane wave space charge model if appropriate_: For use when using plane wave two beam coupling theory. Only available for two coupled plane waves  propagating in xz plane with symmetric incidence angles.

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

_mobile charge density_: This is the density of empty sites in the crystal when in the dark with no photorefractive grating. Its units are m<sup>-3</sup>. Typical values are of the order of 10<sup>22</sup> m<sup>-3</sup>. From Garrett et al[24]: 6.4 x 10<sup>22</sup> m<sup>-3</sup>, and from Feinberg et al[15]: 1.9 x 10<sup>22</sup> m<sup>-3</sup>. 

_temperature K_: Temperature in Kelvin.

_refractive index_: Crystal refractive index. For BaTiO<sub>3</sub>, 2.4 (data available from various sources, with slight differences between ordinary and extraordinary indices).

_dark intensity_: Equivalent optical intensity accounting for thermally ionized carriers. This intensity accounts for dark decay of the gratings. Normalized to the sum of the average peak intensity I<sub>0</sub> of the beams. (See appendix A)

_Tukey window edge_: The edge parameter for the Tukey (cosine taper) window[25] used to enable absorbing boundaries of the propagation lattice in both real space and Fourier space


[^1] N. V. Kukhtarev, V. B. Markov, S. G. Odulov, M. S. Soskin, and V. L. Vinetskii, Ferroelectrics **22**, 949 (1979)
