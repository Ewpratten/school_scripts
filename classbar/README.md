# Classbar

Classbar is a small Python script that adds information about my current course to `i3status` on my laptop. Some example messages include:

 - `Advanced Functions in 10m in room 204`
 - `Advanced Functions ends in 5m. Next: Robotics in room 114H`
 - `Robotics ends in 15m!`

## Usage

Modify the `status_command` line of your `~/.config/i3/config` file to look like this

```
status_command i3status | python3 -u /path/to/school_scripts/classbar/classbar.py
```

The `-u` flag disabled stdio buffering, and is REQUIRED.