Kivy Physics Sandbox
====================

Kivy Physics Sandbox is educational application for visualizing different physics-based experiments.

Experiments are dynamically populated from `experiments` folder. Each experiment must have this folder structure:

    experiments/
      <category>/
        category.json  # Category information: title and icon file
        <experiment_name>
          experiment.json  # Experiment information: title, short description and icon file
          description.rst  # Description in RST format
          experiment.py    # Main experiment file
      
