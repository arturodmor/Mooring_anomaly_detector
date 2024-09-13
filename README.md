# Mooring Anchoring Detection

Anchoring_detection is a customised package of functionalities for the study of signals from floating offshore wind platforms (FOWT). Through simulations of behaviour at sea, it is possible to generate a dataset in order to study a common failure mode of anchor lines: the anchoring (or Dragging) effect.

## Table of contents

- [Description](#Description)
- [Installation](#Installation)
- [Acknowledgements](#Acknowledgements)
- [Contact](#Contact)


## Description

### About anchoring effect

<div align="center">
	<img src="https://github.com/user-attachments/assets/f11f20ad-7a3c-4405-817c-a1787a3080a4">
</div>

Anchoring (or dragging) is a phenomenon that occurs when the forces of the waves overcome the gripping forces of an anchor. This type of failure can have serious consequences, producing increases in tension or even breakage of the anchor line, generating a destabilisation of the position of the platform.

To determine this failure mode, a methodology has been developed to train Machine Learning models capable of detecting it.

### Study hypothesis

The behaviour of a floating platform at sea is a random phenomenon influenced by many effects. It is therefore considered appropriate to comment briefly the boundary conditions of the problem by answering the following questions:

- **What does the platform look like? What are its characteristics? Are more than one type of geometry analysed?** For this first test, the DeepCWind OC4 model validated by the National Renewable Energy Laboratory (NREL) was used. The geometric characteristics of the assembly (tower, float and mooring) can be consulted at the following link. The geometrical characteristics are kept constant, maintaining so far a surrogated model development.

- **Under what conditions has the platform been activated?** As data generation is synthetic, a matrix of simulations has been developed where sea states are grouped according to the area of operation for which the platform is designed. For this first study, only first order wave excitation and the restoring force of anchoring have been considered (the effects of wind and second order waves will be considered in the future). To learn more about how this reasoning was developed, please consult the following document.

- **What operating states have been considered in the anchoring?** For now, the problem is focused on a binary classification, with a healthy anchor state (class 0) and a state of anchoring as a result of varying its anchor position (class 1). For more information on this issue, please refer to the documentation in the link.

- **What movements have been considered so far to train the models?** Analysing the signals experienced by the platform in the different states, a noticeable influence on the movements of Surge and Sway was observed. To see how they are characterised statistically, see the document in the link.

### Concept map

<div align="center">
	<img src="https://github.com/user-attachments/assets/242615b7-7ee8-4367-bf9c-bd96f384fc43">
</div>

- **Simulation stage**: Signals are determined  for each combination of wave type parameters. It is possible to apply an FFT to work also in the frequency domain.

- **Data analysis stage**: The statistical parameters of the waves with and without anchoring are analyzed and compared. In this project, differences were observed when comparing spectral moments (m0), so this parameter was grouped as characteristics for the Surge and Sway movements, obtaining a labeled dataset.

- **Train models stage**: The data is normalized to begin a cross-validation process. Once the models are adjusted, they are trained and subsequently tested with unseen data. The entire process has been carried out accompanied by classic metrics in classification problems.

## Installation

1. If the user wants to isolate dependencies, he can install a virtual environment as follows:
    ```bash
    python -m venv anchoring_detection
    source anchoring_detection/bin/activate  
    # In Windows: anchoring_detection\Scripts\activate
    ```

2. Install dependencies with a conda environment:

    ```bash
    conda env create --name anchoring_detection --file environment.yml
    ```

3. To install in local computer the package anchoring_detection with setup file:
    ```bash
    pip install -e .
    ```

## Acknowledgements

This project has been made possible thanks to the support of the Naval Engineering School of [Polytechnic University of Cartagena (UPCT)](https://navales.upct.es/), with the help of the International [Centre for Numerical Methods in Engineering (CIMNE)](https://www.cimne.com/) and the collaboration of the IT solutions company [HI-Iberia Ingeniería y Proyectos](https://www.hi-iberia.es/).

## Contact

- Mail --> rodriguezmoranarturo@gmail.com
- [LinkedIn](www.linkedin.com/in/arturo-rodríguez-morán)