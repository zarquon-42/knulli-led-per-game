#!/bin/bash

# This script uses gameStart and gameStop events to set the LED settings on a per game basis
 
CMD_GENERATE_GAME_COLOUR="/opt/generate_game_colour.py"
CMD_ANALOG_STICK_LED_DAEMON="/usr/bin/analog_stick_led_daemon.sh"
TRUE=0
FALSE=1

logfile=/tmp/"$(basename "${0%.*}.log")"
create_missing_led_files=$TRUE

function reset_settings(){
    # Reset existing settings
    echo "DEBUG: ${FUNCNAME[0]}: Reset Daemon" | tee -a "$logfile" >/dev/null 2>&1
    $CMD_ANALOG_STICK_LED_DAEMON import 2>&1 | tee -a "$logfile" >/dev/null 2>&1
}

function set_led(){
    local led_setting_file="${1:-$backup_settings_file}"

    if [ -f "${led_setting_file}" ]; then
        return $($CMD_ANALOG_STICK_LED_DAEMON set $(cat "${led_setting_file}"))
    else
        echo "DEBUG: ${FUNCNAME[0]}: led_setting_file ($led_setting_file) does not exist." | tee -a "$logfile" >/dev/null 2>&1
        return 404
    fi
}

function start_game() {
    local rom_path="$1"
    local dirname=${rom_path%/*}
    local basename=${rom_path##*/}
    local name=${basename%.*}
    local led_setting_file="$dirname/default.led"
    if [ -f "$dirname/led/$name.led" ]; then
        led_setting_file="$dirname/led/$name.led"
    else
        if [ $create_missing_led_files -eq $TRUE ] && [ -f "$CMD_GENERATE_GAME_COLOUR" ]; then
            colour=$("$CMD_GENERATE_GAME_COLOUR" "$dirname/images" "$name" 2>/dev/null)
            echo "DEBUG: ${FUNCNAME[0]}: Determined colour: $colour" | tee -a "$logfile" >/dev/null 2>&1

            if [ ! -z "$colour" ]; then
                led_setting_file="$dirname/led/$name.led"
                echo "DEBUG: ${FUNCNAME[0]}: writing colour ($colour) to settings file ($led_setting_file)" | tee -a "$logfile" >/dev/null 2>&1
                [ ! -d "$dirname/led" ] && mkdir -p "$dirname/led"
                echo "$colour" >"$led_setting_file"
            fi
        fi
    fi

    set_led "$led_setting_file"
}

# Case selection for first parameter parsed, our event.
case $1 in
    gameStart)
        # Commands in here will be executed on the start of any game.
        start_game "$5"
    ;;
    gameStop)
        # Commands here will be executed on the stop of every game.
        reset_settings
    ;;
esac
