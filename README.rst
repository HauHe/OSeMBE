OSeMBE
======

This repository cotains:

The Open Source energy Model Base for the European Union (OSeMBE)
-----------------------------------------------------------------

An Energy model base for the European Union developed using the **OSeMOSYS** Modelling Framework.
The model provides country-detailed representation of the 28 European Union (EU) Member States + Switzerland and Norway. The model aims at being used as a multi-regional stakeholders engagement model at the European level.
The development was funded by the European Union’s Horizon 2020 research and innovation programme under grant agreement No 691739.

Setup and Installation
----------------------

To run this analysis you need to install GLPK and a solver such as CBC or CPLEX.
You should also have Python >= 3.6 environment setup with the following dependencies:
- `pandas`
- `plotly`

Folder structure
----------------

- Input data are stored as `datapackages` in the `input_data` folder
- A modified OSeMOSYS model file is stored in the `model` folder

Licensing
---------
- Data is released under the terms of a CC-BY-4.0 International License Agreement.
- A modified copy of OSeMOSYS is redistribruted in this repository under Apache 2.0 license agreement, a copy of which can be found in the `model` folder

Citation
--------

If you wish to use, extend or otherwise build upon the work contained within this repository, you are
welcome to do so, provided you abide by the terms of the licenses detailed above.

Please cite this work in the following manner:
    `Henke, H., 2019, The Open Source energy Modelling Base for Europe (OSeMBE)`