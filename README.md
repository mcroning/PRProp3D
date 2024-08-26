# PRProp3D
The software presented here is a three dimensional photorefractive beam propagation code. It is capable of modelling both static and dynamic interactions.
The menu items are shown below.

![image](https://github.com/user-attachments/assets/bb0ca750-cbe9-40f5-b944-09c42b79222e)

The program calculates unidirectional nonlinear optical beam propagation in three dimensions using photorefractive optical nonlinearities. It is based on the well-known split step beam propagation method which divides the process into a series of alternating steps along the longitudinal z direction. Diffractive propagation steps are handled using the angular spectrum of plane waves method[14] in which the angular spectrum of the optical field is calculated using the Fast Fourier Transform (FFT). The field is propagated as a set of individual plane waves for a short distance dz and the inverse Fourier transform is taken. The accumulated nonlinearity is then calculated from the intensity and applied as a spatially varying transparency. The process is repeated until the end of the interaction region is reached. The parameters used in the code are as follows, listed in the order that they appear in the input form.
The program with its default parameters will work on Google COLAB’s free accounts using its T4 GPU.  
The defaults are two beam coupling of 100 $\mu m$ diameter beams with input angles of $\theta$ = 0.1 radians and $\gamma \ell$ =-3. The longitudinal step size is 20 $\mu m$ and the crystal aperture is 1mm x 1mm. The interaction length is 4mm. A steady state calculation takes about 8 seconds. Time dependent image amplification over 80 steps to an end time of ten time units takes about 10 minutes. The program has also been tested with plane wave coupling with $\gamma \ell$ =-3, beam ratio 1 and fanning with $\gamma \ell$ = 10 and beam ratio zero.

Some examples to try initially:
1) Run with default parameters.  Theis will show steady state two beam coupling of two 100 $\mu m$ waist beams with $\gamma \ell$ =-3. On a T4 this takes about 7 seconds
2) Run the same in time dependent mode. Toggle the time behavior dropdown. Chenge the beam ratio to 6 to get a more pronounced amplification. This will take about ten minutes.
3) Amplify an image. Usse the image on beam dropdown to select 'Beam 1'. Select one of the MNIST images, or an AF resolution target. If yoou choose am MNIST image, I recommend to check the invert image check box. If you want to see the amplified beam seclect "backpropagate image". This is eqiovalent to bringing the amplified image bearing beam to an image plane. You might want to select staic time dependence at first.
4) Model fanning. Set the gain to 10, beam ratio zero, noise type 'volume xy', check 'fanning study'. Without an image applied you should find that the fanning efficiiency is about 33%
5) Repeat the fanning modeling but with beam 1 waist 200 $\mu m$. You will see that the fanning is stronger than with the 100 $\mu m$ waist beam, and artifacts are beginning to creep in. The plot of the transverse gration goild shows that the fields have begun to wrap around and the far field image shows the characteristic artifact rings
   
