# ExperimentWindow

This is the main experiment class.

## Parameters

`time` - when application is in **play** mode (when play button is pressed), this parameter stores current simulation time

`experiment_path` - stores path to experiment folder

`live` - shows if application is in **play** mode

`can_change_speed` - if `True` user can change the speed of simulation (default: `True`)

## Methods

`get_file(file)` - returns full path to `file`. `file` should be relative to experiment folder. You can use this to get path of images or other data.

`load()` - this method is executed when experiment is selected. Use it to build widgets and layout.

`reset()` - this method is executed when user press **Reset** button.

`update(*largs)` - this method is executed when:
    - application is in **play** mode this method is executed every `dt` seconds. `dt` should be `largs[1]`
    - user changes controls' values. This method is executed with default kivy parameters: widget and value.
    You can use `self.live` parameter to change only live values.
    
Simple solution to make both work is this:

```
def update(self, *largs):
    try:
        dt = float(largs[0])
    except:
        dt = 0.0
```

You can also use default kivy method `on_size` to set widgets' sizes and position

## Events

`on_drag(widget, touch)` - fires, when user drag mouse or touch over experiment window