How to run OSeMBE
=================

There are different ways how an OSeMOSYS model can be run. The central choices to make are which `model version` (OSeMOSYS) to use and with which `solver` to solve the model. 

The model choice
----------------

This version of OSeMBE gives CCS technologies as an option, as mentioned in the `README`. Therefore, one needs a version of the OSeMOSYS code that has some minor modifcations. Namely the OSeMOSYS code needs to allow negative emissions. An adjusted OSeMOSYS code can be found here: https://github.com/HauHe/OSeMOSYS_GNU_MathProg/tree/osembe In the folder `src`.

The solver choice
-----------------

We recommend to run OSeMBE using two solver for performing two different steps of the solving process. Below we describe what steps are needed to run OSeMBE:

1. Convert the OSeMBE datapackage to a datafile. For this `otoole` is needed. The conversion can be performed with the command below::

    otoole convert datapackage datafile datapackage.json osembe_data.txt

2. For the second step a solver called **GLPK** is needed. With GLPK we generate a so called `lp`-file. An lp-file can be generated with the following command::

    glpsol -m model/osemosys_fast.txt -d input_data/osembe_data.txt --wlp input_data/osembe.lp --check

3. For solving OSeMBE we recommend the solver **gurobi**. Gurobi can solve the lp-file generated in the previous command with the following command::
    
    gurobi_cl ResultFile=results/issuereport.ilp ResultFile=results/osembe.sol input_data/osembe.lp

4. The solution file `osembe.sol` can be converted to a human readable format with the following command provided to otoole::

    otoole results gurobi csv results/osembe.sol results/ --input_datafile input_data/osembe_data.txt

Gurobi requires a license, which is free for academics. Who doesn't have access to gurobi can work with **CBC**. To run OSeMBE with CBC step 3 and 4 change as shown below.

3. Solving the lp-file with CBC requires the following command::

    cbc input_data/osembe.lp solve -solu results/osembe_solution.txt

4. The command for otoole changes to::

    otoole results cbc csv results/osembe_solution.txt results/ --input_datafile input_data/osembe_data.txt