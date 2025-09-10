# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 11:18:11 2022
@author: meta-cronos
Initialize with and object containing folder-objects, each containing and array
with .md files contained in the folder:

    {
     'folder1':[md-file1, md_file2, md_file3,...etc],
     'folder2':[md-file1, md_file2, md_file3,...etc]
     }
"""
import os
import json
import time
import uuid
import pickle
import shutil
import ffmpy
import jsonpickle
from pathlib import Path
from bs4 import BeautifulSoup
from mrkdwn_analysis import MarkdownAnalyzer
from jinja2 import Environment, FileSystemLoader
from collections import deque
from hvym_stellar import *
from stellar_sdk import Keypair


CSS_LIGHT = """ 

/* Custom Theme for Onsen UI 2.11.2 */



  /* variables for iOS components */

  --background-color: #efeff4;

  --text-color: #1f1f21;

  --sub-text-color: #999;

  --highlight-color: rgba(122,72,169,1);

  --second-highlight-color: rgba(159,122,193,1);

  --border-color: #ccc;

  --button-background-color: var(--highlight-color);

  --button-cta-background-color: var(--second-highlight-color);

  --toolbar-background-color: #fafafa;

  --toolbar-button-color: var(--highlight-color);

  --toolbar-text-color: #1f1f21;

  --toolbar-border-color: #b2b2b2;

  --button-bar-color: var(--highlight-color);

  --button-bar-active-text-color: #fff;

  --button-bar-active-background-color: color-mod(var(--button-bar-color) tint(70%));

  --button-light-color: black;

  --segment-color: var(--highlight-color);

  --segment-active-text-color: #fff;

  --segment-active-background-color: color-mod(var(--segment-color) tint(70%));

  --list-background-color: #fff;

  --list-header-background-color: #eee;

  --list-tap-active-background-color: #d9d9d9;

  --list-item-chevron-color: #c7c7cc;

  --progress-bar-color: var(--highlight-color);

  --progress-bar-secondary-color: rgba(174,119,224,1);

  --progress-bar-background-color: transparent;

  --progress-circle-primary-color: var(--highlight-color);

  --progress-circle-secondary-color: #65adff;

  --progress-circle-background-color: transparent;

  --tabbar-background-color: #fafafa;

  --tabbar-text-color: #999;

  --tabbar-highlight-text-color: var(--highlight-color);

  --tabbar-border-color: #ccc;

  --switch-highlight-color: rgba(210,199,92,1);

  --switch-border-color: #e5e5e5;

  --switch-background-color: white;

  --range-track-background-color: #a4aab3;

  --range-track-background-color-active: var(--highlight-color);

  --range-thumb-background-color: #fff;

  --modal-background-color: rgba(0, 0, 0, 0.7);

  --modal-text-color: #fff;

  --alert-dialog-background-color: #f4f4f4;

  --alert-dialog-text-color: #1f1f21;

  --alert-dialog-button-color: var(--highlight-color);

  --alert-dialog-separator-color: #ddd;

  --dialog-background-color: #f4f4f4;

  --dialog-text-color: var(--text-color);

  --popover-background-color: white;

  --popover-text-color: #1f1f21;

  --action-sheet-title-color: #8f8e94;

  --action-sheet-button-separator-color: rgba(0, 0, 0, 0.1);

  --action-sheet-button-color: var(--highlight-color);

  --action-sheet-button-destructive-color: #fe3824;

  --action-sheet-button-background-color: rgba(255, 255, 255, 0.9);

  --action-sheet-button-active-background-color: #e9e9e9;

  --action-sheet-cancel-button-background-color: #fff;

  --notification-background-color: #7A48A9;

  --notification-color: white;

  --search-input-background-color: rgba(3, 3, 3, 0.09);

  --fab-text-color: #ffffff;

  --fab-background-color: var(--highlight-color);

  --fab-active-background-color: color-mod(var(--fab-background-color) a(70%));

  --card-background-color: white;

  --card-text-color: #030303;

  --toast-background-color: rgba(0, 0, 0, 0.8);

  --toast-text-color: white;

  --toast-button-text-color: white;

  --select-input-color: var(--text-color);

  --select-input-border-color: var(--border-color);



  /* variables for Material Design components */

  --material-background-color: #eceff1;

  --material-text-color: var(--text-color);

  --material-notification-background-color: #7A48A9;

  --material-notification-color: white;

  --material-switch-active-thumb-color: #37474f;

  --material-switch-active-background-color: color-mod(#37474f a(50%));

  --material-switch-inactive-thumb-color: #f1f1f1;

  --material-switch-inactive-background-color: #b0afaf;

  --material-range-track-color: #bdbdbd;

  --material-range-thumb-color: #31313a;

  --material-range-disabled-thumb-color: #b0b0b0;

  --material-range-disabled-thumb-border-color: #eeeeee;

  --material-range-zero-thumb-color: #f2f2f2;

  --material-toolbar-background-color: #ffffff;

  --material-toolbar-text-color: #31313a;

  --material-toolbar-button-color: rgba(163,103,220,1);

  --material-segment-background-color: #fafafa;

  --material-segment-active-background-color: #c8c8c8;

  --material-segment-text-color: color-mod(black a(38%));

  --material-segment-active-text-color: #353535;

  --material-button-background-color: rgba(170,107,228,1);

  --material-button-text-color: #ffffff;

  --material-button-disabled-background-color: color-mod(#4f4f4f a(26%));

  --material-button-disabled-color: color-mod(black a(26%));

  --material-flat-button-active-background-color: color-mod(#999 a(20%));

  --material-list-background-color: #fff;

  --material-list-item-separator-color: #eee;

  --material-list-header-text-color: #757575;

  --material-checkbox-active-color: #37474f;

  --material-checkbox-inactive-color: #717171;

  --material-checkbox-checkmark-color: #ffffff;

  --material-radio-button-active-color: #37474f;

  --material-radio-button-inactive-color: #717171;

  --material-radio-button-disabled-color: #afafaf;

  --material-text-input-text-color: #212121;

  --material-text-input-active-color: #3d5afe;

  --material-text-input-inactive-color: #afafaf;

  --material-search-background-color: #fafafa;

  --material-dialog-background-color: #ffffff;

  --material-dialog-text-color: var(--material-text-color);

  --material-alert-dialog-background-color: #ffffff;

  --material-alert-dialog-title-color: #31313a;

  --material-alert-dialog-content-color: rgba(49, 49, 58, 0.85);

  --material-alert-dialog-button-color: #37474f;

  --material-progress-bar-primary-color: rgba(83,60,105,1);

  --material-progress-bar-secondary-color: rgba(142,98,183,1);

  --material-progress-bar-background-color: transparent;

  --material-progress-circle-primary-color: var(--material-progress-bar-primary-color);

  --material-progress-circle-secondary-color: var(--material-progress-bar-secondary-color);

  --material-progress-circle-background-color: transparent;

  --material-tabbar-background-color: #ffffff;

  --material-tabbar-text-color: #31313a;

  --material-tabbar-highlight-text-color: #31313a;

  --material-tabbar-highlight-color: rgba(49, 49, 58, 0.1);

  --material-fab-text-color: #31313a;

  --material-fab-background-color: #ffffff;

  --material-fab-active-background-color: rgba(255, 255, 255, 0.75);

  --material-card-background-color: white;

  --material-card-text-color: rgba(0, 0, 0, 0.54);

  --material-toast-background-color: rgba(0, 0, 0, 0.8);

  --material-toast-text-color: white;

  --material-toast-button-text-color: #bbdefb;

  --material-select-input-color: var(--material-text-color);

  --material-select-input-active-color: rgba(0, 0, 0, 0.15);

  --material-select-input-inactive-color: rgba(0, 0, 0, 0.81);

  --material-select-border-color: color-mod(black a(12%));

  --material-popover-background-color: #fafafa;

  --material-popover-text-color: var(--material-text-color);

  --material-action-sheet-text-color: #686868;



  /* others */

  --tap-highlight-color: transparent;

"""

CSS_DARK = """

/* Custom Theme for Onsen UI 2.11.2 */

  /* variables for iOS components */

  --background-color: #0d0d0d;

  --text-color: #fff;

  --sub-text-color: #999;

  --highlight-color: #ffa101;

  --second-highlight-color: #da5926;

  --border-color: #242424;

  --button-background-color: var(--highlight-color);

  --button-cta-background-color: var(--second-highlight-color);

  --button-light-color: white;

  --toolbar-background-color: #181818;

  --toolbar-button-color: var(--highlight-color);

  --toolbar-text-color: #fff;

  --toolbar-border-color: #242424;

  --button-bar-color: var(--highlight-color);

  --button-bar-active-text-color: #fff;

  --button-bar-active-background-color: color-mod(var(--button-bar-color) b(80%));

  --segment-color: var(--highlight-color);

  --segment-active-text-color: #fff;

  --segment-active-background-color: color-mod(var(--segment-color) b(80%));

  --list-background-color: #181818;

  --list-header-background-color: #111;

  --list-tap-active-background-color: #262626;

  --list-item-chevron-color: #383833;

  --progress-bar-color: var(--highlight-color);

  --progress-bar-secondary-color: color-mod(var(--progress-bar-color) b(55%));

  --progress-bar-background-color: transparent;

  --progress-circle-primary-color: var(--progress-bar-color);

  --progress-circle-secondary-color: color-mod(var(--progress-bar-secondary-color) b(55%));

  --progress-circle-background-color: transparent;

  --tabbar-background-color: #212121;

  --tabbar-text-color: #aaa;

  --tabbar-highlight-text-color: var(--highlight-color);

  --tabbar-border-color: #0d0d0d;

  --switch-highlight-color: #44db5e;

  --switch-border-color: #666;

  --switch-background-color: var(--background-color);

  --range-track-background-color: #6b6f74;

  --range-track-background-color-active: #bbb;

  --range-thumb-background-color: #fff;

  --modal-background-color: color-mod(black a(70%));

  --modal-text-color: #fff;

  --alert-dialog-background-color: #f4f4f4;

  --alert-dialog-text-color: #1f1f21;

  --alert-dialog-button-color: var(--highlight-color);

  --alert-dialog-separator-color: #ddd;

  --dialog-background-color: #0d0d0d;

  --dialog-text-color: #1f1f21;

  --popover-background-color: #242424;

  --popover-text-color: var(--text-color);

  --action-sheet-title-color: #8f8e94;

  --action-sheet-button-separator-color: rgba(0, 0, 0, 0.1);

  --action-sheet-button-color: var(--highlight-color);

  --action-sheet-button-destructive-color: #fe3824;

  --action-sheet-button-background-color: rgba(255, 255, 255, 0.9);

  --action-sheet-button-active-background-color: #e9e9e9;

  --action-sheet-cancel-button-background-color: #fff;

  --notification-background-color: #fe3824;

  --notification-color: white;

  --search-input-background-color: color-mod(white a(9%));

  --fab-text-color: #ffffff;

  --fab-background-color: var(--highlight-color);

  --fab-active-background-color: color-mod(var(--fab-background-color) a(70%));

  --card-background-color: var(--border-color);

  --card-text-color: var(--text-color);

  --toast-background-color: #ccc;

  --toast-text-color: #000;

  --toast-button-text-color: #000;

  --select-input-color: var(--text-color);

  --select-input-border-color: var(--border-color);



  /* variables for Material Design components */

  --material-background-color: #303030;

  --material-text-color: #ffffff;

  --material-notification-background-color: #f50057;

  --material-notification-color: white;

  --material-switch-active-thumb-color: #ffc107;

  --material-switch-active-background-color: color-mod(var(--material-switch-active-thumb-color) a(50%));

  --material-switch-inactive-thumb-color: #bdbdbd;

  --material-switch-inactive-background-color: color-mod(white a(30%));

  --material-range-track-color: #525252;

  --material-range-thumb-color: #cecec5;

  --material-range-disabled-thumb-color: #4f4f4f;

  --material-range-disabled-thumb-border-color: #303030;

  --material-range-zero-thumb-color: #0d0d0d;

  --material-toolbar-background-color: #212121;

  --material-toolbar-text-color: #ffffff;

  --material-toolbar-button-color: var(--toolbar-button-color);

  --material-segment-background-color: #292929;

  --material-segment-active-background-color: #404040;

  --material-segment-text-color: color-mod(#fff a(62%));

  --material-segment-active-text-color: #cacaca;

  --material-button-background-color: #d68600;

  --material-button-text-color: #ffffff;

  --material-button-disabled-background-color: color-mod(#b0b0b0 a(74%));

  --material-button-disabled-color: color-mod(white a(74%));

  --material-flat-button-active-background-color: color-mod(#666666 a(20%));

  --material-list-background-color: color-mod(var(--material-background-color) l(+2%));

  --material-list-item-separator-color: color-mod(white a(12%));

  --material-list-header-text-color: #8a8a8a;

  --material-checkbox-active-color: #fff;

  --material-checkbox-inactive-color: #717171;

  --material-checkbox-checkmark-color: #000;

  --material-radio-button-active-color: #ffa101;

  --material-radio-button-inactive-color: #8e8e8e;

  --material-radio-button-disabled-color: #505050;

  --material-text-input-text-color: color-mod(#fff a(75%));

  --material-text-input-active-color: color-mod(#fff a(75%));

  --material-text-input-inactive-color: color-mod(#fff a(30%));

  --material-search-background-color: #424242;

  --material-dialog-background-color: #424242;

  --material-dialog-text-color: var(--material-text-color);

  --material-alert-dialog-background-color: #424242;

  --material-alert-dialog-title-color: white;

  --material-alert-dialog-content-color: color-mod(var(--material-alert-dialog-title-color) a(85%));

  --material-alert-dialog-button-color: #d68600;

  --material-progress-bar-primary-color: #d68600;

  --material-progress-bar-secondary-color: color-mod(var(--material-progress-bar-primary-color) b(55%));

  --material-progress-bar-background-color: transparent;

  --material-progress-circle-primary-color: var(--material-progress-bar-primary-color);

  --material-progress-circle-secondary-color: var(--material-progress-bar-secondary-color);

  --material-progress-circle-background-color: transparent;

  --material-tabbar-background-color: var(--material-toolbar-background-color);

  --material-tabbar-text-color: color-mod(var(--material-toolbar-text-color) a(50%));

  --material-tabbar-highlight-text-color: var(--material-toolbar-text-color);

  --material-tabbar-highlight-color: color-mod(var(--material-toolbar-background-color) l(+3%));

  --material-fab-text-color: #31313a;

  --material-fab-background-color: #ffffff;

  --material-fab-active-background-color: color-mod(white a(75%));

  --material-card-background-color: #424242;

  --material-card-text-color: color-mod(white a(46%));

  --material-toast-background-color: #ccc;

  --material-toast-text-color: #000;

  --material-toast-button-text-color: #583905;

  --material-select-input-color: var(--material-text-color);

  --material-select-input-active-color: color-mod(white a(85%));

  --material-select-input-inactive-color: color-mod(white a(19%));

  --material-select-border-color: color-mod(white a(88%));

  --material-popover-background-color: var(--material-alert-dialog-background-color);

  --material-popover-text-color: var(--material-text-color);

  --material-action-sheet-text-color: #686868;



  /* others */

  --tap-highlight-color: transparent;

"""

CSS_HEAVYMETA = """

 /* variables for iOS components */

  --background-color: #98314A;

  --text-color: #fff;

  --sub-text-color: #999;

  --highlight-color: #31B09C;

  --second-highlight-color: rgba(133,230,215,1);

  --border-color: rgba(210,110,134,1);

  --button-background-color: var(--highlight-color);

  --button-cta-background-color: var(--second-highlight-color);

  --button-light-color: white;

  --toolbar-background-color: #181818;

  --toolbar-button-color: var(--highlight-color);

  --toolbar-text-color: #fff;

  --toolbar-border-color: #242424;

  --button-bar-color: rgba(106,224,205,1);

  --button-bar-active-text-color: #fff;

  --button-bar-active-background-color: color-mod(var(--button-bar-color) b(80%));

  --segment-color: rgba(99,188,174,1);

  --segment-active-text-color: #fff;

  --segment-active-background-color: color-mod(var(--segment-color) b(80%));

  --list-background-color: #181818;

  --list-header-background-color: #111;

  --list-tap-active-background-color: #262626;

  --list-item-chevron-color: #383833;

  --progress-bar-color: var(--highlight-color);

  --progress-bar-secondary-color: color-mod(var(--progress-bar-color) b(55%));

  --progress-bar-background-color: transparent;

  --progress-circle-primary-color: var(--progress-bar-color);

  --progress-circle-secondary-color: color-mod(var(--progress-bar-secondary-color) b(55%));

  --progress-circle-background-color: transparent;

  --tabbar-background-color: #212121;

  --tabbar-text-color: #aaa;

  --tabbar-highlight-text-color: var(--highlight-color);

  --tabbar-border-color: #0d0d0d;

  --switch-highlight-color: #44db5e;

  --switch-border-color: #666;

  --switch-background-color: var(--background-color);

  --range-track-background-color: #6b6f74;

  --range-track-background-color-active: #bbb;

  --range-thumb-background-color: #fff;

  --modal-background-color: color-mod(black a(70%));

  --modal-text-color: #fff;

  --alert-dialog-background-color: #f4f4f4;

  --alert-dialog-text-color: #1f1f21;

  --alert-dialog-button-color: var(--highlight-color);

  --alert-dialog-separator-color: #ddd;

  --dialog-background-color: #0d0d0d;

  --dialog-text-color: #1f1f21;

  --popover-background-color: #242424;

  --popover-text-color: var(--text-color);

  --action-sheet-title-color: #8f8e94;

  --action-sheet-button-separator-color: rgba(0, 0, 0, 0.1);

  --action-sheet-button-color: var(--highlight-color);

  --action-sheet-button-destructive-color: #fe3824;

  --action-sheet-button-background-color: rgba(255, 255, 255, 0.9);

  --action-sheet-button-active-background-color: #e9e9e9;

  --action-sheet-cancel-button-background-color: #fff;

  --notification-background-color: #fe3824;

  --notification-color: white;

  --search-input-background-color: color-mod(white a(9%));

  --fab-text-color: #ffffff;

  --fab-background-color: var(--highlight-color);

  --fab-active-background-color: color-mod(var(--fab-background-color) a(70%));

  --card-background-color: var(--border-color);

  --card-text-color: var(--text-color);

  --toast-background-color: #ccc;

  --toast-text-color: #000;

  --toast-button-text-color: #000;

  --select-input-color: var(--text-color);

  --select-input-border-color: var(--border-color);



  /* variables for Material Design components */

  --material-background-color: #98314A;

  --material-text-color: #ffffff;

  --material-notification-background-color: #f50057;

  --material-notification-color: white;

  --material-switch-active-thumb-color: rgba(212,102,128,1);

  --material-switch-active-background-color: color-mod(var(--material-switch-active-thumb-color) a(50%));

  --material-switch-inactive-thumb-color: #bdbdbd;

  --material-switch-inactive-background-color: color-mod(white a(30%));

  --material-range-track-color: #525252;

  --material-range-thumb-color: #cecec5;

  --material-range-disabled-thumb-color: #4f4f4f;

  --material-range-disabled-thumb-border-color: #303030;

  --material-range-zero-thumb-color: #0d0d0d;

  --material-toolbar-background-color: #212121;

  --material-toolbar-text-color: #ffffff;

  --material-toolbar-button-color: var(--toolbar-button-color);

  --material-segment-background-color: #292929;

  --material-segment-active-background-color: #404040;

  --material-segment-text-color: color-mod(#fff a(62%));

  --material-segment-active-text-color: #cacaca;

  --material-button-background-color: #d68600;

  --material-button-text-color: #ffffff;

  --material-button-disabled-background-color: color-mod(#b0b0b0 a(74%));

  --material-button-disabled-color: color-mod(white a(74%));

  --material-flat-button-active-background-color: color-mod(#666666 a(20%));

  --material-list-background-color: color-mod(var(--material-background-color) l(+2%));

  --material-list-item-separator-color: color-mod(white a(12%));

  --material-list-header-text-color: #8a8a8a;

  --material-checkbox-active-color: #fff;

  --material-checkbox-inactive-color: #717171;

  --material-checkbox-checkmark-color: #000;

  --material-radio-button-active-color: #31B09C;

  --material-radio-button-inactive-color: #8e8e8e;

  --material-radio-button-disabled-color: #505050;

  --material-text-input-text-color: color-mod(#fff a(75%));

  --material-text-input-active-color: color-mod(#fff a(75%));

  --material-text-input-inactive-color: color-mod(#fff a(30%));

  --material-search-background-color: #424242;

  --material-dialog-background-color: #424242;

  --material-dialog-text-color: var(--material-text-color);

  --material-alert-dialog-background-color: #424242;

  --material-alert-dialog-title-color: white;

  --material-alert-dialog-content-color: color-mod(var(--material-alert-dialog-title-color) a(85%));

  --material-alert-dialog-button-color: #d68600;

  --material-progress-bar-primary-color: #31B09C;

  --material-progress-bar-secondary-color: color-mod(var(--material-progress-bar-primary-color) b(55%));

  --material-progress-bar-background-color: transparent;

  --material-progress-circle-primary-color: var(--material-progress-bar-primary-color);

  --material-progress-circle-secondary-color: var(--material-progress-bar-secondary-color);

  --material-progress-circle-background-color: transparent;

  --material-tabbar-background-color: var(--material-toolbar-background-color);

  --material-tabbar-text-color: color-mod(var(--material-toolbar-text-color) a(50%));

  --material-tabbar-highlight-text-color: var(--material-toolbar-text-color);

  --material-tabbar-highlight-color: color-mod(var(--material-toolbar-background-color) l(+3%));

  --material-fab-text-color: #31313a;

  --material-fab-background-color: #ffffff;

  --material-fab-active-background-color: color-mod(white a(75%));

  --material-card-background-color: #424242;

  --material-card-text-color: color-mod(white a(46%));

  --material-toast-background-color: #ccc;

  --material-toast-text-color: #000;

  --material-toast-button-text-color: #583905;

  --material-select-input-color: var(--material-text-color);

  --material-select-input-active-color: color-mod(white a(85%));

  --material-select-input-inactive-color: color-mod(white a(19%));

  --material-select-border-color: color-mod(white a(88%));

  --material-popover-background-color: var(--material-alert-dialog-background-color);

  --material-popover-text-color: var(--material-text-color);

  --material-action-sheet-text-color: #686868;



  /* others */

  --tap-highlight-color: transparent;

"""

CSS_CRIMSON = """

  /* variables for iOS components */

  --background-color: rgba(84,25,39,1);

  --text-color: rgba(230,41,41,1);

  --sub-text-color: rgba(212,88,88,1);

  --highlight-color: rgba(255,17,17,1);

  --second-highlight-color: rgba(241,70,70,1);

  --border-color: rgba(138,8,39,1);

  --button-background-color: var(--highlight-color);

  --button-cta-background-color: var(--second-highlight-color);

  --button-light-color: white;

  --toolbar-background-color: #181818;

  --toolbar-button-color: var(--highlight-color);

  --toolbar-text-color: rgba(222,0,0,1);

  --toolbar-border-color: #242424;

  --button-bar-color: hsl(0,65.55%,64.70%);

  --button-bar-active-text-color: #fff;

  --button-bar-active-background-color: color-mod(var(--button-bar-color) b(80%));

  --segment-color: hsl(0,39.91%,56.27%);

  --segment-active-text-color: #fff;

  --segment-active-background-color: color-mod(var(--segment-color) b(80%));

  --list-background-color: #181818;

  --list-header-background-color: #111;

  --list-tap-active-background-color: #262626;

  --list-item-chevron-color: #383833;

  --progress-bar-color: var(--highlight-color);

  --progress-bar-secondary-color: color-mod(var(--progress-bar-color) b(55%));

  --progress-bar-background-color: transparent;

  --progress-circle-primary-color: var(--progress-bar-color);

  --progress-circle-secondary-color: color-mod(var(--progress-bar-secondary-color) b(55%));

  --progress-circle-background-color: transparent;

  --tabbar-background-color: #212121;

  --tabbar-text-color: #aaa;

  --tabbar-highlight-text-color: var(--highlight-color);

  --tabbar-border-color: #0d0d0d;

  --switch-highlight-color: #44db5e;

  --switch-border-color: #666;

  --switch-background-color: var(--background-color);

  --range-track-background-color: #6b6f74;

  --range-track-background-color-active: #bbb;

  --range-thumb-background-color: #fff;

  --modal-background-color: color-mod(black a(70%));

  --modal-text-color: #fff;

  --alert-dialog-background-color: rgba(212,172,172,1);

  --alert-dialog-text-color: #1f1f21;

  --alert-dialog-button-color: var(--highlight-color);

  --alert-dialog-separator-color: #ddd;

  --dialog-background-color: #0d0d0d;

  --dialog-text-color: #1f1f21;

  --popover-background-color: #242424;

  --popover-text-color: var(--text-color);

  --action-sheet-title-color: rgba(231,10,10,1);

  --action-sheet-button-separator-color: rgba(0, 0, 0, 0.1);

  --action-sheet-button-color: var(--highlight-color);

  --action-sheet-button-destructive-color: #fe3824;

  --action-sheet-button-background-color: rgba(231,203,203,0.9);

  --action-sheet-button-active-background-color: #D4ACAC;

  --action-sheet-cancel-button-background-color: rgba(244,225,225,1);

  --notification-background-color: #fe3824;

  --notification-color: white;

  --search-input-background-color: color-mod(white a(9%));

  --fab-text-color: #ffffff;

  --fab-background-color: var(--highlight-color);

  --fab-active-background-color: color-mod(var(--fab-background-color) a(70%));

  --card-background-color: var(--border-color);

  --card-text-color: var(--text-color);

  --toast-background-color: rgba(255,118,118,1);

  --toast-text-color: #830404;

  --toast-button-text-color: #000;

  --select-input-color: var(--text-color);

  --select-input-border-color: var(--border-color);



  /* variables for Material Design components */

  --material-background-color: #541927;

  --material-text-color: #E62929;

  --material-notification-background-color: #f50057;

  --material-notification-color: white;

  --material-switch-active-thumb-color: rgba(212,102,128,1);

  --material-switch-active-background-color: color-mod(var(--material-switch-active-thumb-color) a(50%));

  --material-switch-inactive-thumb-color: #bdbdbd;

  --material-switch-inactive-background-color: color-mod(white a(30%));

  --material-range-track-color: #525252;

  --material-range-thumb-color: #cecec5;

  --material-range-disabled-thumb-color: #4f4f4f;

  --material-range-disabled-thumb-border-color: #303030;

  --material-range-zero-thumb-color: #0d0d0d;

  --material-toolbar-background-color: #212121;

  --material-toolbar-text-color: rgba(236,4,4,1);

  --material-toolbar-button-color: var(--toolbar-button-color);

  --material-segment-background-color: hsl(360,0.00%,16.07%);

  --material-segment-active-background-color: #404040;

  --material-segment-text-color: color-mod(#fff a(62%));

  --material-segment-active-text-color: #cacaca;

  --material-button-background-color: hsl(0,100.00%,41.96%);

  --material-button-text-color: #ffffff;

  --material-button-disabled-background-color: color-mod(#b0b0b0 a(74%));

  --material-button-disabled-color: color-mod(white a(74%));

  --material-flat-button-active-background-color: color-mod(#666666 a(20%));

  --material-list-background-color: color-mod(var(--material-background-color) l(+2%));

  --material-list-item-separator-color: color-mod(white a(12%));

  --material-list-header-text-color: #8a8a8a;

  --material-checkbox-active-color: #fff;

  --material-checkbox-inactive-color: #717171;

  --material-checkbox-checkmark-color: #000;

  --material-radio-button-active-color: hsl(0,56.44%,44.11%);

  --material-radio-button-inactive-color: #8e8e8e;

  --material-radio-button-disabled-color: #505050;

  --material-text-input-text-color: color-mod(#fff a(75%));

  --material-text-input-active-color: color-mod(#fff a(75%));

  --material-text-input-inactive-color: color-mod(#fff a(30%));

  --material-search-background-color: #424242;

  --material-dialog-background-color: #424242;

  --material-dialog-text-color: var(--material-text-color);

  --material-alert-dialog-background-color: rgba(149,38,38,1);

  --material-alert-dialog-title-color: white;

  --material-alert-dialog-content-color: color-mod(var(--material-alert-dialog-title-color) a(85%));

  --material-alert-dialog-button-color: hsl(0,100.00%,41.96%);

  --material-progress-bar-primary-color: hsl(0,56.44%,44.11%);

  --material-progress-bar-secondary-color: color-mod(var(--material-progress-bar-primary-color) b(55%));

  --material-progress-bar-background-color: transparent;

  --material-progress-circle-primary-color: var(--material-progress-bar-primary-color);

  --material-progress-circle-secondary-color: var(--material-progress-bar-secondary-color);

  --material-progress-circle-background-color: transparent;

  --material-tabbar-background-color: var(--material-toolbar-background-color);

  --material-tabbar-text-color: color-mod(var(--material-toolbar-text-color) a(50%));

  --material-tabbar-highlight-text-color: var(--material-toolbar-text-color);

  --material-tabbar-highlight-color: color-mod(var(--material-toolbar-background-color) l(+3%));

  --material-fab-text-color: #31313a;

  --material-fab-background-color: #ffffff;

  --material-fab-active-background-color: color-mod(white a(75%));

  --material-card-background-color: #424242;

  --material-card-text-color: color-mod(white a(46%));

  --material-toast-background-color: #FF7676;

  --material-toast-text-color: #830404;

  --material-toast-button-text-color: rgba(131,4,4,1);

  --material-select-input-color: var(--material-text-color);

  --material-select-input-active-color: color-mod(white a(85%));

  --material-select-input-inactive-color: color-mod(white a(19%));

  --material-select-border-color: color-mod(white a(88%));

  --material-popover-background-color: var(--material-alert-dialog-background-color);

  --material-popover-text-color: var(--material-text-color);

  --material-action-sheet-text-color: rgba(208,79,79,1);



  /* others */

  --tap-highlight-color: transparent;

"""

CSS_BLUE = """

  /* variables for iOS components */

  --background-color: hsl(208.94,54.11%,21.37%);

  --text-color: hsl(218.35,82.90%,67.84%);

  --sub-text-color: hsl(223.06,59.04%,58.82%);

  --highlight-color: rgba(104,142,239,1);

  --second-highlight-color: rgba(34,80,220,1);

  --border-color: hsl(218.35,89.04%,28.62%);

  --button-background-color: var(--highlight-color);

  --button-cta-background-color: rgba(52,94,224,1);

  --button-light-color: white;

  --toolbar-background-color: #181818;

  --toolbar-button-color: var(--highlight-color);

  --toolbar-text-color: hsl(208.94,100.00%,43.52%);

  --toolbar-border-color: #242424;

  --button-bar-color: hsl(216,65.55%,64.70%);

  --button-bar-active-text-color: #fff;

  --button-bar-active-background-color: color-mod(var(--button-bar-color) b(80%));

  --segment-color: hsl(199.53,39.90%,56.27%);

  --segment-active-text-color: #fff;

  --segment-active-background-color: color-mod(var(--segment-color) b(80%));

  --list-background-color: #181818;

  --list-header-background-color: #111;

  --list-tap-active-background-color: #262626;

  --list-item-chevron-color: #383833;

  --progress-bar-color: var(--highlight-color);

  --progress-bar-secondary-color: color-mod(var(--progress-bar-color) b(55%));

  --progress-bar-background-color: transparent;

  --progress-circle-primary-color: var(--progress-bar-color);

  --progress-circle-secondary-color: color-mod(var(--progress-bar-secondary-color) b(55%));

  --progress-circle-background-color: transparent;

  --tabbar-background-color: #212121;

  --tabbar-text-color: #aaa;

  --tabbar-highlight-text-color: var(--highlight-color);

  --tabbar-border-color: #0d0d0d;

  --switch-highlight-color: #44db5e;

  --switch-border-color: #666;

  --switch-background-color: var(--background-color);

  --range-track-background-color: #6b6f74;

  --range-track-background-color-active: #bbb;

  --range-thumb-background-color: #fff;

  --modal-background-color: color-mod(black a(70%));

  --modal-text-color: #fff;

  --alert-dialog-background-color: hsl(211.29,31.74%,75.29%);

  --alert-dialog-text-color: #1f1f21;

  --alert-dialog-button-color: var(--highlight-color);

  --alert-dialog-separator-color: hsl(230.12,0.00%,86.66%);

  --dialog-background-color: #0d0d0d;

  --dialog-text-color: #1f1f21;

  --popover-background-color: #242424;

  --popover-text-color: var(--text-color);

  --action-sheet-title-color: hsl(213.65,91.69%,47.25%);

  --action-sheet-button-separator-color: rgba(0, 0, 0, 0.1);

  --action-sheet-button-color: var(--highlight-color);

  --action-sheet-button-destructive-color: hsl(220.71,99.08%,56.86%);

  --action-sheet-button-background-color: hsl(218.35,36.84%,85.09%);

  --action-sheet-button-active-background-color: hsl(216,31.74%,75.29%);

  --action-sheet-cancel-button-background-color: hsl(216,46.33%,91.96%);

  --notification-background-color: hsl(220.71,99.09%,56.86%);

  --notification-color: white;

  --search-input-background-color: color-mod(white a(9%));

  --fab-text-color: #ffffff;

  --fab-background-color: var(--highlight-color);

  --fab-active-background-color: color-mod(var(--fab-background-color) a(70%));

  --card-background-color: rgba(44,81,146,1);

  --card-text-color: hsl(208.94,62.56%,66.47%);

  --toast-background-color: hsl(218.35,100.00%,73.13%);

  --toast-text-color: hsl(213.65,94.07%,26.47%);

  --toast-button-text-color: #000;

  --select-input-color: var(--text-color);

  --select-input-border-color: var(--border-color);



  /* variables for Material Design components */

  --material-background-color: hsl(213.65,54.11%,21.37%);

  --material-text-color: hsl(220.71,65.11%,66.27%);

  --material-notification-background-color: hsl(227.76,100.00%,48.03%);

  --material-notification-color: white;

  --material-switch-active-thumb-color: hsl(208.94,56.12%,61.56%);

  --material-switch-active-background-color: color-mod(var(--material-switch-active-thumb-color) a(50%));

  --material-switch-inactive-thumb-color: #bdbdbd;

  --material-switch-inactive-background-color: color-mod(white a(30%));

  --material-range-track-color: #525252;

  --material-range-thumb-color: #cecec5;

  --material-range-disabled-thumb-color: #4f4f4f;

  --material-range-disabled-thumb-border-color: #303030;

  --material-range-zero-thumb-color: #0d0d0d;

  --material-toolbar-background-color: #212121;

  --material-toolbar-text-color: hsl(216,96.66%,47.05%);

  --material-toolbar-button-color: var(--toolbar-button-color);

  --material-segment-background-color: hsl(360,0.00%,16.07%);

  --material-segment-active-background-color: #404040;

  --material-segment-text-color: color-mod(#fff a(62%));

  --material-segment-active-text-color: #cacaca;

  --material-button-background-color: hsl(225.41,30.57%,47.45%);

  --material-button-text-color: hsl(201.88,0.00%,64.42%);

  --material-button-disabled-background-color: color-mod(#b0b0b0 a(74%));

  --material-button-disabled-color: color-mod(white a(74%));

  --material-flat-button-active-background-color: color-mod(#666666 a(20%));

  --material-list-background-color: color-mod(var(--material-background-color) l(+2%));

  --material-list-item-separator-color: color-mod(white a(12%));

  --material-list-header-text-color: #8a8a8a;

  --material-checkbox-active-color: #fff;

  --material-checkbox-inactive-color: #717171;

  --material-checkbox-checkmark-color: #000;

  --material-radio-button-active-color: rgba(138,144,202,1);

  --material-radio-button-inactive-color: #8e8e8e;

  --material-radio-button-disabled-color: #505050;

  --material-text-input-text-color: color-mod(#fff a(75%));

  --material-text-input-active-color: color-mod(#fff a(75%));

  --material-text-input-inactive-color: color-mod(#fff a(30%));

  --material-search-background-color: #424242;

  --material-dialog-background-color: rgba(35,38,56,1);

  --material-dialog-text-color: var(--material-text-color);

  --material-alert-dialog-background-color: rgba(126,149,192,1);

  --material-alert-dialog-title-color: white;

  --material-alert-dialog-content-color: color-mod(var(--material-alert-dialog-title-color) a(85%));

  --material-alert-dialog-button-color: hsl(213.65,100.00%,41.96%);

  --material-progress-bar-primary-color: hsl(230.12,56.44%,44.11%);

  --material-progress-bar-secondary-color: color-mod(var(--material-progress-bar-primary-color) b(55%));

  --material-progress-bar-background-color: transparent;

  --material-progress-circle-primary-color: var(--material-progress-bar-primary-color);

  --material-progress-circle-secondary-color: var(--material-progress-bar-secondary-color);

  --material-progress-circle-background-color: transparent;

  --material-tabbar-background-color: var(--material-toolbar-background-color);

  --material-tabbar-text-color: color-mod(var(--material-toolbar-text-color) a(50%));

  --material-tabbar-highlight-text-color: hsl(208.94,96.66%,47.05%);

  --material-tabbar-highlight-color: color-mod(var(--material-toolbar-background-color) l(+3%));

  --material-fab-text-color: #31313a;

  --material-fab-background-color: #ffffff;

  --material-fab-active-background-color: color-mod(white a(75%));

  --material-card-background-color: #424242;

  --material-card-text-color: color-mod(white a(46%));

  --material-toast-background-color: hsl(218.35,100.00%,73.13%);

  --material-toast-text-color: hsl(220.71,94.07%,26.47%);

  --material-toast-button-text-color: hsl(204.24,94.07%,26.47%);

  --material-select-input-color: var(--material-text-color);

  --material-select-input-active-color: color-mod(white a(85%));

  --material-select-input-inactive-color: color-mod(white a(19%));

  --material-select-border-color: color-mod(white a(88%));

  --material-popover-background-color: hsl(218.35,59.35%,36.65%);

  --material-popover-text-color: var(--material-text-color);

  --material-action-sheet-text-color: hsl(218.35,57.84%,56.27%);



  /* others */

  --tap-highlight-color: transparent;

"""

CSS_JADED = """

  /* variables for iOS components */

  --background-color: hsl(88.94,54.11%,21.37%);

  --text-color: rgba(202,225,164,1);

  --sub-text-color: #8A9C6A;

  --highlight-color: #8A9C6A;

  --second-highlight-color: #8A9C6A;

  --border-color: hsl(77.18,89.04%,28.62%);

  --button-background-color: var(--highlight-color);

  --button-cta-background-color: hsl(86.59,73.50%,54.11%);

  --button-light-color: white;

  --toolbar-background-color: #181818;

  --toolbar-button-color: var(--highlight-color);

  --toolbar-text-color: hsl(81.88,100.00%,43.52%);

  --toolbar-border-color: #242424;

  --button-bar-color: hsl(86.59,65.55%,64.70%);

  --button-bar-active-text-color: rgba(235,252,194,1);

  --button-bar-active-background-color: color-mod(var(--button-bar-color) b(80%));

  --segment-color: hsl(81.88,39.90%,56.27%);

  --segment-active-text-color: #fff;

  --segment-active-background-color: color-mod(var(--segment-color) b(80%));

  --list-background-color: #181818;

  --list-header-background-color: #111;

  --list-tap-active-background-color: #262626;

  --list-item-chevron-color: #383833;

  --progress-bar-color: var(--highlight-color);

  --progress-bar-secondary-color: color-mod(var(--progress-bar-color) b(55%));

  --progress-bar-background-color: transparent;

  --progress-circle-primary-color: var(--progress-bar-color);

  --progress-circle-secondary-color: color-mod(var(--progress-bar-secondary-color) b(55%));

  --progress-circle-background-color: transparent;

  --tabbar-background-color: #212121;

  --tabbar-text-color: #aaa;

  --tabbar-highlight-text-color: var(--highlight-color);

  --tabbar-border-color: #0d0d0d;

  --switch-highlight-color: #44db5e;

  --switch-border-color: #666;

  --switch-background-color: var(--background-color);

  --range-track-background-color: #6b6f74;

  --range-track-background-color-active: #bbb;

  --range-thumb-background-color: #fff;

  --modal-background-color: color-mod(black a(70%));

  --modal-text-color: #fff;

  --alert-dialog-background-color: rgba(209,216,196,1);

  --alert-dialog-text-color: #1f1f21;

  --alert-dialog-button-color: var(--highlight-color);

  --alert-dialog-separator-color: hsl(230.12,0.00%,86.66%);

  --dialog-background-color: rgba(183,204,152,1);

  --dialog-text-color: hsl(86.59,3.12%,12.54%);

  --popover-background-color: #242424;

  --popover-text-color: var(--text-color);

  --action-sheet-title-color: rgba(255,255,255,1);

  --action-sheet-button-separator-color: rgba(0, 0, 0, 0.1);

  --action-sheet-button-color: var(--highlight-color);

  --action-sheet-button-destructive-color: rgba(255,255,255,1);

  --action-sheet-button-background-color: rgba(190,202,176,1);

  --action-sheet-button-active-background-color: rgba(166,190,153,1);

  --action-sheet-cancel-button-background-color: rgba(219,225,212,1);

  --notification-background-color: rgba(149,160,127,1);

  --notification-color: white;

  --search-input-background-color: color-mod(white a(9%));

  --fab-text-color: #ffffff;

  --fab-background-color: var(--highlight-color);

  --fab-active-background-color: color-mod(var(--fab-background-color) a(70%));

  --card-background-color: hsl(74.82,53.68%,37.25%);

  --card-text-color: hsl(70.12,62.56%,66.47%);

  --toast-background-color: hsl(79.53,100.00%,73.13%);

  --toast-text-color: hsl(81.88,94.07%,26.47%);

  --toast-button-text-color: #000;

  --select-input-color: var(--text-color);

  --select-input-border-color: var(--border-color);



  /* variables for Material Design components */

  --material-background-color: hsl(72.47,54.11%,21.37%);

  --material-text-color: #8A9C6A;

  --material-notification-background-color: #95A07F;

  --material-notification-color: white;

  --material-switch-active-thumb-color: hsl(86.59,56.12%,61.56%);

  --material-switch-active-background-color: color-mod(var(--material-switch-active-thumb-color) a(50%));

  --material-switch-inactive-thumb-color: #bdbdbd;

  --material-switch-inactive-background-color: color-mod(white a(30%));

  --material-range-track-color: #525252;

  --material-range-thumb-color: #cecec5;

  --material-range-disabled-thumb-color: #4f4f4f;

  --material-range-disabled-thumb-border-color: #303030;

  --material-range-zero-thumb-color: #0d0d0d;

  --material-toolbar-background-color: #212121;

  --material-toolbar-text-color: hsl(79.53,96.66%,47.05%);

  --material-toolbar-button-color: var(--toolbar-button-color);

  --material-segment-background-color: hsl(360,0.00%,16.07%);

  --material-segment-active-background-color: #404040;

  --material-segment-text-color: color-mod(#fff a(62%));

  --material-segment-active-text-color: #cacaca;

  --material-button-background-color: hsl(86.59,30.57%,47.45%);

  --material-button-text-color: rgba(255,255,255,1);

  --material-button-disabled-background-color: color-mod(#b0b0b0 a(74%));

  --material-button-disabled-color: color-mod(white a(74%));

  --material-flat-button-active-background-color: color-mod(#666666 a(20%));

  --material-list-background-color: color-mod(var(--material-background-color) l(+2%));

  --material-list-item-separator-color: color-mod(white a(12%));

  --material-list-header-text-color: #8a8a8a;

  --material-checkbox-active-color: #fff;

  --material-checkbox-inactive-color: #717171;

  --material-checkbox-checkmark-color: #000;

  --material-radio-button-active-color: rgba(138,144,202,1);

  --material-radio-button-inactive-color: #8e8e8e;

  --material-radio-button-disabled-color: #505050;

  --material-text-input-text-color: color-mod(#fff a(75%));

  --material-text-input-active-color: color-mod(#fff a(75%));

  --material-text-input-inactive-color: color-mod(#fff a(30%));

  --material-search-background-color: #424242;

  --material-dialog-background-color: hsl(77.18,23.07%,17.84%);

  --material-dialog-text-color: var(--material-text-color);

  --material-alert-dialog-background-color: #D1D8C4;

  --material-alert-dialog-title-color: white;

  --material-alert-dialog-content-color: color-mod(var(--material-alert-dialog-title-color) a(85%));

  --material-alert-dialog-button-color: rgba(86,120,14,1);

  --material-progress-bar-primary-color: hsl(81.88,56.44%,44.11%);

  --material-progress-bar-secondary-color: color-mod(var(--material-progress-bar-primary-color) b(55%));

  --material-progress-bar-background-color: transparent;

  --material-progress-circle-primary-color: hsl(81.88,56.44%,44.11%);

  --material-progress-circle-secondary-color: var(--material-progress-bar-secondary-color);

  --material-progress-circle-background-color: transparent;

  --material-tabbar-background-color: var(--material-toolbar-background-color);

  --material-tabbar-text-color: color-mod(var(--material-toolbar-text-color) a(50%));

  --material-tabbar-highlight-text-color: hsl(77.18,96.66%,47.05%);

  --material-tabbar-highlight-color: color-mod(var(--material-toolbar-background-color) l(+3%));

  --material-fab-text-color: #31313a;

  --material-fab-background-color: #ffffff;

  --material-fab-active-background-color: color-mod(white a(75%));

  --material-card-background-color: hsl(81.88,0.00%,25.88%);

  --material-card-text-color: color-mod(white a(46%));

  --material-toast-background-color: hsl(77.18,100.00%,73.13%);

  --material-toast-text-color: hsl(74.82,94.07%,26.47%);

  --material-toast-button-text-color: hsl(77.18,94.07%,26.47%);

  --material-select-input-color: var(--material-text-color);

  --material-select-input-active-color: color-mod(white a(85%));

  --material-select-input-inactive-color: color-mod(white a(19%));

  --material-select-border-color: color-mod(white a(88%));

  --material-popover-background-color: rgba(194,205,176,1);

  --material-popover-text-color: var(--material-text-color);

  --material-action-sheet-text-color: hsl(84.24,57.84%,56.27%);



  /* others */

  --tap-highlight-color: transparent;

"""

CSS_GOLDEN = """

  /* variables for iOS components */

  --background-color: #C6A122;

  --text-color: rgba(255,217,50,1);

  --sub-text-color: rgba(241,241,241,1);

  --highlight-color: rgba(140,112,64,1);

  --second-highlight-color: rgba(255,208,0,1);

  --border-color: rgba(130,117,11,1);

  --button-background-color: rgba(0,0,0,1);

  --button-cta-background-color: rgba(46,39,6,1);

  --button-light-color: rgba(221,221,221,1);

  --toolbar-background-color: #181818;

  --toolbar-button-color: var(--highlight-color);

  --toolbar-text-color: #fff;

  --toolbar-border-color: #242424;

  --button-bar-color: rgba(114,77,13,1);

  --button-bar-active-text-color: rgba(249,249,249,1);

  --button-bar-active-background-color: color-mod(var(--button-bar-color) b(80%));

  --segment-color: var(--highlight-color);

  --segment-active-text-color: #fff;

  --segment-active-background-color: color-mod(var(--segment-color) b(80%));

  --list-background-color: #181818;

  --list-header-background-color: #111;

  --list-tap-active-background-color: #262626;

  --list-item-chevron-color: #383833;

  --progress-bar-color: var(--highlight-color);

  --progress-bar-secondary-color: color-mod(var(--progress-bar-color) b(55%));

  --progress-bar-background-color: transparent;

  --progress-circle-primary-color: var(--progress-bar-color);

  --progress-circle-secondary-color: color-mod(var(--progress-bar-secondary-color) b(55%));

  --progress-circle-background-color: transparent;

  --tabbar-background-color: #212121;

  --tabbar-text-color: #aaa;

  --tabbar-highlight-text-color: var(--highlight-color);

  --tabbar-border-color: #0d0d0d;

  --switch-highlight-color: #44db5e;

  --switch-border-color: #666;

  --switch-background-color: var(--background-color);

  --range-track-background-color: #6b6f74;

  --range-track-background-color-active: #bbb;

  --range-thumb-background-color: #fff;

  --modal-background-color: color-mod(black a(70%));

  --modal-text-color: #fff;

  --alert-dialog-background-color: rgba(0,0,0,1);

  --alert-dialog-text-color: rgba(204,168,84,1);

  --alert-dialog-button-color: var(--highlight-color);

  --alert-dialog-separator-color: rgba(247,216,75,0.42);

  --dialog-background-color: #0d0d0d;

  --dialog-text-color: #1f1f21;

  --popover-background-color: #242424;

  --popover-text-color: var(--text-color);

  --action-sheet-title-color: #8f8e94;

  --action-sheet-button-separator-color: rgba(255,198,0,0.41);

  --action-sheet-button-color: rgba(255,160,1,1);

  --action-sheet-button-destructive-color: #fe3824;

  --action-sheet-button-background-color: rgba(5,5,5,0.9);

  --action-sheet-button-active-background-color: rgba(77,77,77,1);

  --action-sheet-cancel-button-background-color: rgba(129,129,129,1);

  --notification-background-color: rgba(0,0,0,1);

  --notification-color: white;

  --search-input-background-color: color-mod(white a(9%));

  --fab-text-color: #ffffff;

  --fab-background-color: var(--highlight-color);

  --fab-active-background-color: color-mod(var(--fab-background-color) a(70%));

  --card-background-color: var(--border-color);

  --card-text-color: rgba(255,168,0,1);

  --toast-background-color: #ccc;

  --toast-text-color: #000;

  --toast-button-text-color: #000;

  --select-input-color: var(--text-color);

  --select-input-border-color: var(--border-color);



  /* variables for Material Design components */

  --material-background-color: rgba(198,161,34,1);

  --material-text-color: rgba(255,255,255,1);

  --material-notification-background-color: rgba(0,0,0,1);

  --material-notification-color: white;

  --material-switch-active-thumb-color: #ffc107;

  --material-switch-active-background-color: color-mod(var(--material-switch-active-thumb-color) a(50%));

  --material-switch-inactive-thumb-color: #bdbdbd;

  --material-switch-inactive-background-color: color-mod(white a(30%));

  --material-range-track-color: #525252;

  --material-range-thumb-color: #cecec5;

  --material-range-disabled-thumb-color: #4f4f4f;

  --material-range-disabled-thumb-border-color: #303030;

  --material-range-zero-thumb-color: #0d0d0d;

  --material-toolbar-background-color: #212121;

  --material-toolbar-text-color: #ffffff;

  --material-toolbar-button-color: var(--toolbar-button-color);

  --material-segment-background-color: #292929;

  --material-segment-active-background-color: #404040;

  --material-segment-text-color: color-mod(#fff a(62%));

  --material-segment-active-text-color: #cacaca;

  --material-button-background-color: rgba(0,0,0,1);

  --material-button-text-color: rgba(242,242,242,1);

  --material-button-disabled-background-color: color-mod(#b0b0b0 a(74%));

  --material-button-disabled-color: color-mod(white a(74%));

  --material-flat-button-active-background-color: color-mod(#666666 a(20%));

  --material-list-background-color: color-mod(var(--material-background-color) l(+2%));

  --material-list-item-separator-color: color-mod(white a(12%));

  --material-list-header-text-color: #8a8a8a;

  --material-checkbox-active-color: #fff;

  --material-checkbox-inactive-color: #717171;

  --material-checkbox-checkmark-color: #000;

  --material-radio-button-active-color: #ffa101;

  --material-radio-button-inactive-color: #8e8e8e;

  --material-radio-button-disabled-color: #505050;

  --material-text-input-text-color: color-mod(#fff a(75%));

  --material-text-input-active-color: color-mod(#fff a(75%));

  --material-text-input-inactive-color: color-mod(#fff a(30%));

  --material-search-background-color: #424242;

  --material-dialog-background-color: #424242;

  --material-dialog-text-color: var(--material-text-color);

  --material-alert-dialog-background-color: #424242;

  --material-alert-dialog-title-color: white;

  --material-alert-dialog-content-color: rgba(175,174,174,1);

  --material-alert-dialog-button-color: #d68600;

  --material-progress-bar-primary-color: #FFA000;

  --material-progress-bar-secondary-color: color-mod(var(--material-progress-bar-primary-color) b(55%));

  --material-progress-bar-background-color: transparent;

  --material-progress-circle-primary-color: rgba(255,160,0,1);

  --material-progress-circle-secondary-color: var(--material-progress-bar-secondary-color);

  --material-progress-circle-background-color: transparent;

  --material-tabbar-background-color: var(--material-toolbar-background-color);

  --material-tabbar-text-color: color-mod(var(--material-toolbar-text-color) a(50%));

  --material-tabbar-highlight-text-color: var(--material-toolbar-text-color);

  --material-tabbar-highlight-color: color-mod(var(--material-toolbar-background-color) l(+3%));

  --material-fab-text-color: #31313a;

  --material-fab-background-color: #ffffff;

  --material-fab-active-background-color: color-mod(white a(75%));

  --material-card-background-color: #424242;

  --material-card-text-color: color-mod(white a(46%));

  --material-toast-background-color: #ccc;

  --material-toast-text-color: #000;

  --material-toast-button-text-color: #583905;

  --material-select-input-color: var(--material-text-color);

  --material-select-input-active-color: color-mod(white a(85%));

  --material-select-input-inactive-color: color-mod(white a(19%));

  --material-select-border-color: color-mod(white a(88%));

  --material-popover-background-color: var(--material-alert-dialog-background-color);

  --material-popover-text-color: var(--material-text-color);

  --material-action-sheet-text-color: #686868;



  /* others */

  --tap-highlight-color: transparent;

"""

CSS_MANDARIN = """

  /* variables for iOS components */

  --background-color: rgba(237,145,78,1);

  --text-color: rgba(255,255,255,1);

  --sub-text-color: rgba(255,218,166,1);

  --highlight-color: rgba(140,112,64,1);

  --second-highlight-color: rgba(255,134,71,1);

  --border-color: rgba(255,200,93,0.54);

  --button-background-color: #213A01;

  --button-cta-background-color: rgba(46,39,6,1);

  --button-light-color: rgba(195,195,195,1);

  --toolbar-background-color: #181818;

  --toolbar-button-color: hsl(140.71,37.25%,40.00%);

  --toolbar-text-color: rgba(255,128,0,1);

  --toolbar-border-color: #242424;

  --button-bar-color: hsl(143.06,79.52%,24.90%);

  --button-bar-active-text-color: rgba(255,128,0,1);

  --button-bar-active-background-color: color-mod(var(--button-bar-color) b(80%));

  --segment-color: var(--highlight-color);

  --segment-active-text-color: #fff;

  --segment-active-background-color: color-mod(var(--segment-color) b(80%));

  --list-background-color: rgba(255,128,0,1);

  --list-header-background-color: rgba(25,64,0,1);

  --list-tap-active-background-color: #262626;

  --list-item-chevron-color: #383833;

  --progress-bar-color: var(--highlight-color);

  --progress-bar-secondary-color: color-mod(var(--progress-bar-color) b(55%));

  --progress-bar-background-color: transparent;

  --progress-circle-primary-color: var(--progress-bar-color);

  --progress-circle-secondary-color: color-mod(var(--progress-bar-secondary-color) b(55%));

  --progress-circle-background-color: transparent;

  --tabbar-background-color: #212121;

  --tabbar-text-color: rgba(1,105,53,1);

  --tabbar-highlight-text-color: #FF8E09;

  --tabbar-border-color: #0d0d0d;

  --switch-highlight-color: #44db5e;

  --switch-border-color: #666;

  --switch-background-color: var(--background-color);

  --range-track-background-color: #6b6f74;

  --range-track-background-color-active: #bbb;

  --range-thumb-background-color: #fff;

  --modal-background-color: color-mod(black a(70%));

  --modal-text-color: #fff;

  --alert-dialog-background-color: rgba(23,36,0,1);

  --alert-dialog-text-color: rgba(204,168,84,1);

  --alert-dialog-button-color: var(--highlight-color);

  --alert-dialog-separator-color: rgba(255,98,0,0.67);

  --dialog-background-color: #0d0d0d;

  --dialog-text-color: #1f1f21;

  --popover-background-color: rgba(19,43,0,1);

  --popover-text-color: var(--text-color);

  --action-sheet-title-color: #8f8e94;

  --action-sheet-button-separator-color: rgba(255,198,0,0.53);

  --action-sheet-button-color: rgba(255,160,1,1);

  --action-sheet-button-destructive-color: #fe3824;

  --action-sheet-button-background-color: rgba(5,5,5,0.9);

  --action-sheet-button-active-background-color: rgba(39,39,39,1);

  --action-sheet-cancel-button-background-color: rgba(129,129,129,1);

  --notification-background-color: rgba(0,0,0,1);

  --notification-color: white;

  --search-input-background-color: color-mod(white a(9%));

  --fab-text-color: #ffffff;

  --fab-background-color: var(--highlight-color);

  --fab-active-background-color: color-mod(var(--fab-background-color) a(70%));

  --card-background-color: rgba(37,54,2,1);

  --card-text-color: rgba(255,168,0,1);

  --toast-background-color: #A5B7AB;

  --toast-text-color: #000;

  --toast-button-text-color: #000;

  --select-input-color: var(--text-color);

  --select-input-border-color: var(--border-color);



  /* variables for Material Design components */

  --material-background-color: #ED914E;

  --material-text-color: rgba(255,255,255,1);

  --material-notification-background-color: rgba(0,0,0,1);

  --material-notification-color: white;

  --material-switch-active-thumb-color: hsl(27.76,100.00%,51.36%);

  --material-switch-active-background-color: color-mod(var(--material-switch-active-thumb-color) a(50%));

  --material-switch-inactive-thumb-color: #bdbdbd;

  --material-switch-inactive-background-color: color-mod(white a(30%));

  --material-range-track-color: #525252;

  --material-range-thumb-color: #cecec5;

  --material-range-disabled-thumb-color: #4f4f4f;

  --material-range-disabled-thumb-border-color: #303030;

  --material-range-zero-thumb-color: #0d0d0d;

  --material-toolbar-background-color: #212121;

  --material-toolbar-text-color: rgba(255,138,0,1);

  --material-toolbar-button-color: var(--toolbar-button-color);

  --material-segment-background-color: #292929;

  --material-segment-active-background-color: #404040;

  --material-segment-text-color: color-mod(#fff a(62%));

  --material-segment-active-text-color: #cacaca;

  --material-button-background-color: rgba(33,58,1,1);

  --material-button-text-color: rgba(255,99,0,1);

  --material-button-disabled-background-color: color-mod(#b0b0b0 a(74%));

  --material-button-disabled-color: color-mod(white a(74%));

  --material-flat-button-active-background-color: color-mod(#666666 a(20%));

  --material-list-background-color: color-mod(var(--material-background-color) l(+2%));

  --material-list-item-separator-color: color-mod(white a(12%));

  --material-list-header-text-color: #8a8a8a;

  --material-checkbox-active-color: #fff;

  --material-checkbox-inactive-color: rgba(28,86,0,1);

  --material-checkbox-checkmark-color: #1C5600;

  --material-radio-button-active-color: #ffa101;

  --material-radio-button-inactive-color: #8e8e8e;

  --material-radio-button-disabled-color: #505050;

  --material-text-input-text-color: color-mod(#fff a(75%));

  --material-text-input-active-color: color-mod(#fff a(75%));

  --material-text-input-inactive-color: color-mod(#fff a(30%));

  --material-search-background-color: #424242;

  --material-dialog-background-color: #424242;

  --material-dialog-text-color: var(--material-text-color);

  --material-alert-dialog-background-color: #424242;

  --material-alert-dialog-title-color: rgba(7,7,7,1);

  --material-alert-dialog-content-color: rgba(175,174,174,1);

  --material-alert-dialog-button-color: hsl(27.76,100.00%,41.96%);

  --material-progress-bar-primary-color: #FFA000;

  --material-progress-bar-secondary-color: color-mod(var(--material-progress-bar-primary-color) b(55%));

  --material-progress-bar-background-color: transparent;

  --material-progress-circle-primary-color: rgba(255,160,0,1);

  --material-progress-circle-secondary-color: var(--material-progress-bar-secondary-color);

  --material-progress-circle-background-color: transparent;

  --material-tabbar-background-color: var(--material-toolbar-background-color);

  --material-tabbar-text-color: color-mod(var(--material-toolbar-text-color) a(50%));

  --material-tabbar-highlight-text-color: #FF8E09;

  --material-tabbar-highlight-color: color-mod(var(--material-toolbar-background-color) l(+3%));

  --material-fab-text-color: #31313a;

  --material-fab-background-color: #ffffff;

  --material-fab-active-background-color: color-mod(white a(75%));

  --material-card-background-color: rgba(44,54,18,1);

  --material-card-text-color: color-mod(white a(46%));

  --material-toast-background-color: rgba(165,183,171,1);

  --material-toast-text-color: #000;

  --material-toast-button-text-color: #583905;

  --material-select-input-color: var(--material-text-color);

  --material-select-input-active-color: color-mod(white a(85%));

  --material-select-input-inactive-color: color-mod(white a(19%));

  --material-select-border-color: color-mod(white a(88%));

  --material-popover-background-color: #132B00;

  --material-popover-text-color: var(--material-text-color);

  --material-action-sheet-text-color: #686868;



  /* others */

  --tap-highlight-color: transparent;

"""

CSS_OGONBATTO = """

  /* variables for iOS components */

  --background-color: #0d0d0d;

  --text-color: #fff;

  --sub-text-color: #999;

  --highlight-color: rgba(122,72,169,1);

  --second-highlight-color: rgba(159,122,193,1);

  --border-color: #242424;

  --button-background-color: var(--highlight-color);

  --button-cta-background-color: var(--second-highlight-color);

  --button-light-color: white;

  --toolbar-background-color: #181818;

  --toolbar-button-color: var(--highlight-color);

  --toolbar-text-color: #fff;

  --toolbar-border-color: #242424;

  --button-bar-color: var(--highlight-color);

  --button-bar-active-text-color: #fff;

  --button-bar-active-background-color: color-mod(var(--button-bar-color) b(80%));

  --segment-color: var(--highlight-color);

  --segment-active-text-color: #fff;

  --segment-active-background-color: color-mod(var(--segment-color) b(80%));

  --list-background-color: #181818;

  --list-header-background-color: #111;

  --list-tap-active-background-color: #262626;

  --list-item-chevron-color: #383833;

  --progress-bar-color: var(--highlight-color);

  --progress-bar-secondary-color: rgba(174,119,224,1);

  --progress-bar-background-color: transparent;

  --progress-circle-primary-color: var(--progress-bar-color);

  --progress-circle-secondary-color: color-mod(var(--progress-bar-secondary-color) b(55%));

  --progress-circle-background-color: transparent;

  --tabbar-background-color: #212121;

  --tabbar-text-color: #aaa;

  --tabbar-highlight-text-color: var(--highlight-color);

  --tabbar-border-color: #0d0d0d;

  --switch-highlight-color: rgba(210,199,92,1);

  --switch-border-color: #666;

  --switch-background-color: var(--background-color);

  --range-track-background-color: #6b6f74;

  --range-track-background-color-active: #bbb;

  --range-thumb-background-color: #fff;

  --modal-background-color: color-mod(black a(70%));

  --modal-text-color: #fff;

  --alert-dialog-background-color: #f4f4f4;

  --alert-dialog-text-color: #1f1f21;

  --alert-dialog-button-color: var(--highlight-color);

  --alert-dialog-separator-color: #ddd;

  --dialog-background-color: #0d0d0d;

  --dialog-text-color: #1f1f21;

  --popover-background-color: #242424;

  --popover-text-color: var(--text-color);

  --action-sheet-title-color: #8f8e94;

  --action-sheet-button-separator-color: rgba(0, 0, 0, 0.1);

  --action-sheet-button-color: var(--highlight-color);

  --action-sheet-button-destructive-color: #fe3824;

  --action-sheet-button-background-color: rgba(255, 255, 255, 0.9);

  --action-sheet-button-active-background-color: #e9e9e9;

  --action-sheet-cancel-button-background-color: #fff;

  --notification-background-color: #7A48A9;

  --notification-color: white;

  --search-input-background-color: color-mod(white a(9%));

  --fab-text-color: #ffffff;

  --fab-background-color: var(--highlight-color);

  --fab-active-background-color: color-mod(var(--fab-background-color) a(70%));

  --card-background-color: var(--border-color);

  --card-text-color: var(--text-color);

  --toast-background-color: #ccc;

  --toast-text-color: #000;

  --toast-button-text-color: #000;

  --select-input-color: var(--text-color);

  --select-input-border-color: var(--border-color);



  /* variables for Material Design components */

  --material-background-color: #303030;

  --material-text-color: #ffffff;

  --material-notification-background-color: #7A48A9;

  --material-notification-color: white;

  --material-switch-active-thumb-color: #ffc107;

  --material-switch-active-background-color: color-mod(var(--material-switch-active-thumb-color) a(50%));

  --material-switch-inactive-thumb-color: #bdbdbd;

  --material-switch-inactive-background-color: color-mod(white a(30%));

  --material-range-track-color: #525252;

  --material-range-thumb-color: #cecec5;

  --material-range-disabled-thumb-color: #4f4f4f;

  --material-range-disabled-thumb-border-color: #303030;

  --material-range-zero-thumb-color: #0d0d0d;

  --material-toolbar-background-color: #212121;

  --material-toolbar-text-color: #ffffff;

  --material-toolbar-button-color: rgba(163,103,220,1);

  --material-segment-background-color: #292929;

  --material-segment-active-background-color: #404040;

  --material-segment-text-color: color-mod(#fff a(62%));

  --material-segment-active-text-color: #cacaca;

  --material-button-background-color: rgba(170,107,228,1);

  --material-button-text-color: #ffffff;

  --material-button-disabled-background-color: color-mod(#b0b0b0 a(74%));

  --material-button-disabled-color: color-mod(white a(74%));

  --material-flat-button-active-background-color: color-mod(#666666 a(20%));

  --material-list-background-color: color-mod(var(--material-background-color) l(+2%));

  --material-list-item-separator-color: color-mod(white a(12%));

  --material-list-header-text-color: #8a8a8a;

  --material-checkbox-active-color: #fff;

  --material-checkbox-inactive-color: #717171;

  --material-checkbox-checkmark-color: #000;

  --material-radio-button-active-color: #ffa101;

  --material-radio-button-inactive-color: #8e8e8e;

  --material-radio-button-disabled-color: #505050;

  --material-text-input-text-color: color-mod(#fff a(75%));

  --material-text-input-active-color: color-mod(#fff a(75%));

  --material-text-input-inactive-color: color-mod(#fff a(30%));

  --material-search-background-color: #424242;

  --material-dialog-background-color: #424242;

  --material-dialog-text-color: var(--material-text-color);

  --material-alert-dialog-background-color: #424242;

  --material-alert-dialog-title-color: white;

  --material-alert-dialog-content-color: color-mod(var(--material-alert-dialog-title-color) a(85%));

  --material-alert-dialog-button-color: #d68600;

  --material-progress-bar-primary-color: rgba(83,60,105,1);

  --material-progress-bar-secondary-color: rgba(142,98,183,1);

  --material-progress-bar-background-color: transparent;

  --material-progress-circle-primary-color: var(--material-progress-bar-primary-color);

  --material-progress-circle-secondary-color: var(--material-progress-bar-secondary-color);

  --material-progress-circle-background-color: transparent;

  --material-tabbar-background-color: var(--material-toolbar-background-color);

  --material-tabbar-text-color: color-mod(var(--material-toolbar-text-color) a(50%));

  --material-tabbar-highlight-text-color: var(--material-toolbar-text-color);

  --material-tabbar-highlight-color: color-mod(var(--material-toolbar-background-color) l(+3%));

  --material-fab-text-color: #31313a;

  --material-fab-background-color: #ffffff;

  --material-fab-active-background-color: color-mod(white a(75%));

  --material-card-background-color: #424242;

  --material-card-text-color: color-mod(white a(46%));

  --material-toast-background-color: #ccc;

  --material-toast-text-color: #000;

  --material-toast-button-text-color: #583905;

  --material-select-input-color: var(--material-text-color);

  --material-select-input-active-color: color-mod(white a(85%));

  --material-select-input-inactive-color: color-mod(white a(19%));

  --material-select-border-color: color-mod(white a(88%));

  --material-popover-background-color: var(--material-alert-dialog-background-color);

  --material-popover-text-color: var(--material-text-color);

  --material-action-sheet-text-color: #686868;



  /* others */

  --tap-highlight-color: transparent;

"""

CSS_VAMPIRE = """

  /* variables for iOS components */

  --background-color: #0d0d0d;

  --text-color: #B8BCE8;

  --sub-text-color: #999;

  --highlight-color: rgba(136,115,208,1);

  --second-highlight-color: #da5926;

  --border-color: #242424;

  --button-background-color: rgba(255,1,1,0.85);

  --button-cta-background-color: hsl(0,70.86%,50.19%);

  --button-light-color: white;

  --toolbar-background-color: #181818;

  --toolbar-button-color: var(--highlight-color);

  --toolbar-text-color: #fff;

  --toolbar-border-color: #242424;

  --button-bar-color: hsl(0,100.00%,50.20%);

  --button-bar-active-text-color: #B8BCE8;

  --button-bar-active-background-color: color-mod(var(--button-bar-color) b(80%));

  --segment-color: var(--highlight-color);

  --segment-active-text-color: #fff;

  --segment-active-background-color: color-mod(var(--segment-color) b(80%));

  --list-background-color: #181818;

  --list-header-background-color: #111;

  --list-tap-active-background-color: #262626;

  --list-item-chevron-color: hsl(0,100.00%,76.48%);

  --progress-bar-color: var(--highlight-color);

  --progress-bar-secondary-color: color-mod(var(--progress-bar-color) b(55%));

  --progress-bar-background-color: transparent;

  --progress-circle-primary-color: var(--progress-bar-color);

  --progress-circle-secondary-color: color-mod(var(--progress-bar-secondary-color) b(55%));

  --progress-circle-background-color: transparent;

  --tabbar-background-color: #212121;

  --tabbar-text-color: #aaa;

  --tabbar-highlight-text-color: var(--highlight-color);

  --tabbar-border-color: #0d0d0d;

  --switch-highlight-color: #44db5e;

  --switch-border-color: #666;

  --switch-background-color: var(--background-color);

  --range-track-background-color: #6b6f74;

  --range-track-background-color-active: #bbb;

  --range-thumb-background-color: #fff;

  --modal-background-color: color-mod(black a(70%));

  --modal-text-color: #fff;

  --alert-dialog-background-color: rgba(102,102,142,1);

  --alert-dialog-text-color: rgba(168,160,238,1);

  --alert-dialog-button-color: rgba(198,97,97,1);

  --alert-dialog-separator-color: rgba(251,0,0,0.48);

  --dialog-background-color: #0d0d0d;

  --dialog-text-color: #1f1f21;

  --popover-background-color: #242424;

  --popover-text-color: var(--text-color);

  --action-sheet-title-color: #8f8e94;

  --action-sheet-button-separator-color: rgba(255,0,0,0.29);

  --action-sheet-button-color: var(--highlight-color);

  --action-sheet-button-destructive-color: #fe3824;

  --action-sheet-button-background-color: rgba(73,71,95,0.9);

  --action-sheet-button-active-background-color: rgba(59,61,99,1);

  --action-sheet-cancel-button-background-color: rgba(76,72,108,1);

  --notification-background-color: rgba(255,24,0,1);

  --notification-color: rgba(15,15,15,1);

  --search-input-background-color: color-mod(white a(9%));

  --fab-text-color: #ffffff;

  --fab-background-color: var(--highlight-color);

  --fab-active-background-color: color-mod(var(--fab-background-color) a(70%));

  --card-background-color: var(--border-color);

  --card-text-color: var(--text-color);

  --toast-background-color: #ccc;

  --toast-text-color: #000;

  --toast-button-text-color: #000;

  --select-input-color: var(--text-color);

  --select-input-border-color: var(--border-color);



  /* variables for Material Design components */

  --material-background-color: #303030;

  --material-text-color: #B8BCE8;

  --material-notification-background-color: rgba(255,0,91,1);

  --material-notification-color: rgba(0,0,0,1);

  --material-switch-active-thumb-color: hsl(256,50.10%,59.39%);

  --material-switch-active-background-color: color-mod(var(--material-switch-active-thumb-color) a(50%));

  --material-switch-inactive-thumb-color: #bdbdbd;

  --material-switch-inactive-background-color: color-mod(white a(30%));

  --material-range-track-color: #525252;

  --material-range-thumb-color: #cecec5;

  --material-range-disabled-thumb-color: #4f4f4f;

  --material-range-disabled-thumb-border-color: #303030;

  --material-range-zero-thumb-color: #0d0d0d;

  --material-toolbar-background-color: #212121;

  --material-toolbar-text-color: #ffffff;

  --material-toolbar-button-color: var(--toolbar-button-color);

  --material-segment-background-color: #292929;

  --material-segment-active-background-color: #404040;

  --material-segment-text-color: color-mod(#fff a(62%));

  --material-segment-active-text-color: #cacaca;

  --material-button-background-color: hsl(0,100.00%,41.96%);

  --material-button-text-color: rgba(184,188,232,1);

  --material-button-disabled-background-color: color-mod(#b0b0b0 a(74%));

  --material-button-disabled-color: color-mod(white a(74%));

  --material-flat-button-active-background-color: color-mod(#666666 a(20%));

  --material-list-background-color: rgba(37,31,31,1);

  --material-list-item-separator-color: rgba(255,0,0,1);

  --material-list-header-text-color: rgba(255,0,0,1);

  --material-checkbox-active-color: #fff;

  --material-checkbox-inactive-color: #717171;

  --material-checkbox-checkmark-color: #000;

  --material-radio-button-active-color: hsl(0,100.00%,50.20%);

  --material-radio-button-inactive-color: #8e8e8e;

  --material-radio-button-disabled-color: #505050;

  --material-text-input-text-color: color-mod(#fff a(75%));

  --material-text-input-active-color: color-mod(#fff a(75%));

  --material-text-input-inactive-color: color-mod(#fff a(30%));

  --material-search-background-color: #424242;

  --material-dialog-background-color: #424242;

  --material-dialog-text-color: var(--material-text-color);

  --material-alert-dialog-background-color: #424242;

  --material-alert-dialog-title-color: rgba(203,110,110,1);

  --material-alert-dialog-content-color: color-mod(var(--material-alert-dialog-title-color) a(85%));

  --material-alert-dialog-button-color: rgba(166,161,209,1);

  --material-progress-bar-primary-color: hsl(0,100.00%,50.00%);

  --material-progress-bar-secondary-color: color-mod(var(--material-progress-bar-primary-color) b(55%));

  --material-progress-bar-background-color: transparent;

  --material-progress-circle-primary-color: var(--material-progress-bar-primary-color);

  --material-progress-circle-secondary-color: var(--material-progress-bar-secondary-color);

  --material-progress-circle-background-color: transparent;

  --material-tabbar-background-color: var(--material-toolbar-background-color);

  --material-tabbar-text-color: color-mod(var(--material-toolbar-text-color) a(50%));

  --material-tabbar-highlight-text-color: var(--material-toolbar-text-color);

  --material-tabbar-highlight-color: color-mod(var(--material-toolbar-background-color) l(+3%));

  --material-fab-text-color: #31313a;

  --material-fab-background-color: #ffffff;

  --material-fab-active-background-color: color-mod(white a(75%));

  --material-card-background-color: #424242;

  --material-card-text-color: color-mod(white a(46%));

  --material-toast-background-color: #ccc;

  --material-toast-text-color: #000;

  --material-toast-button-text-color: #583905;

  --material-select-input-color: var(--material-text-color);

  --material-select-input-active-color: color-mod(white a(85%));

  --material-select-input-inactive-color: color-mod(white a(19%));

  --material-select-border-color: color-mod(white a(88%));

  --material-popover-background-color: var(--material-alert-dialog-background-color);

  --material-popover-text-color: var(--material-text-color);

  --material-action-sheet-text-color: #686868;



  /* others */

  --tap-highlight-color: rgba(148,153,255,0.37);

"""


SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))


HOME_PATH = str(Path.home())


file_loader = FileSystemLoader("templates")


env = Environment(loader=file_loader)


class SiteDataHandler:
    "Class for handling site data."

    def __init__(self, filePath, MarkdownHandler, W3DeployHandler):

        self.filePath = filePath

        self.distPath = os.path.join(SCRIPT_DIR, "dist")

        self.pageList = []

        self.folders = {}

        self.folderData = {}

        self.pageData = {}

        self.columnWidths = {}

        self.articleData = {}

        self.articleOrder = {}

        self.formData = {}

        self.metaData = {}

        self.opensea_metadata = """{

  "description": "", 
  "external_url": "", 
  "image": "", 
  "name": "",
  "attributes": []
}
      """

        self.css_themes = {
            "light": CSS_LIGHT,
            "dark": CSS_DARK,
            "heavymeta": CSS_HEAVYMETA,
            "crimson-tide": CSS_CRIMSON,
            "deep-blue": CSS_BLUE,
            "golden-crown": CSS_GOLDEN,
            "somewhat-jaded": CSS_JADED,
            "mandarin-logos": CSS_MANDARIN,
            "ogon-batto": CSS_OGONBATTO,
            "vexxed-vampire": CSS_VAMPIRE,
        }

        self.css_components = CSS_DARK

        # Font system

        self.popular_google_fonts = {
            "Sans Serif": [
                "Roboto",
                "Open Sans",
                "Lato",
                "Inter",
                "Source Sans Pro",
                "Ubuntu",
                "Nunito",
                "Work Sans",
                "PT Sans",
                "Raleway",
            ],
            "Serif": [
                "Merriweather",
                "Playfair Display",
                "Lora",
                "Crimson Text",
                "Source Serif Pro",
                "Libre Baskerville",
                "Noto Serif",
            ],
            "Display": [
                "Montserrat",
                "Oswald",
                "Poppins",
                "Bebas Neue",
                "Abril Fatface",
                "Pacifico",
                "Dancing Script",
                "Great Vibes",
            ],
            "Monospace": [
                "Roboto Mono",
                "Source Code Pro",
                "Fira Code",
                "JetBrains Mono",
                "Inconsolata",
                "Space Mono",
            ],
        }

        self.settings = {
            "css_components": self.css_components,
            "uiFramework": "onsen",
            "pageType": "splitter",
            "menuSide": "right",
            "style": "default",
            "row_pad": 5,
            "deployType": "Pintheon",
            "theme": "light",
            "siteName": "dist",
            "mediaDir": "_resources",
            "description": "",
            "siteID": uuid.uuid4().hex,
            "customTheme": "",
            "pintheon_access_token": "",
            "backend_end_point": "https://127.0.0.1:9999",
            "backend_timeout": 100,
            "nft_site_type": "None",
            "nft_type": "None",
            "nft_metadata_standard": "None",
            "nft_start_supply": 1024,
            "nft_contract": "",
            "site_metadata": self.opensea_metadata,
            "project_name": os.path.basename(self.filePath),
            "deploy_type": "Pintheon",
            "private_key": "",
            "customFonts": {
                "primary": {
                    "family": "Roboto",
                    "source": "google",
                    "weights": [300, 400, 500, 700],
                    "fallback": "Arial, sans-serif",
                },
                "heading": {
                    "family": "Montserrat",
                    "source": "google",
                    "weights": [400, 600, 700],
                    "fallback": "Helvetica, Arial, sans-serif",
                },
            },
            "fontSettings": {"enableCustomFonts": True, "fontDisplay": "swap"},
        }

        # Set resourcePath after settings is initialized

        self.resourcePath = os.path.join(
            self.filePath, self.settings.get("mediaDir", "_resources")
        )

        self.authors = {}

        self.uiFramework = ["onsen"]

        self.navigation = ["splitter", "tabs", "carousel"]

        self.themes = list(self.css_themes.keys())

        self.styles = ["default", "outlined", "material",  "material outlined"]

        self.deployTypes = ["Pintheon"]

        self.nftTypes = ["None", "Dero", "Beam"]

        self.nftMetadata_standards = ["None", "Opensea"]

        self.nftSiteTypes = ["None", "Site-NFT", "Collection-Minter"]

        self.nftStartSupply = 1024

        self.dataFilePath = os.path.join(filePath, "site.data")

        self.dataBakFilePath = os.path.join(filePath, "siteBak.data")

        self.fileExists = False

        self.resourcesExist = False

        self.oldFolders = []

        self.oldDataFolders = []

        self.oldDataKeys = []

        self.templateDebug = "template_index.txt"

        self.markdownHandler = MarkdownHandler.MarkdownHandler(filePath)

        self.markdownHandler.setMediaDir(self.settings.get("mediaDir", "_resources"))

        self.debugPath = os.path.join(SCRIPT_DIR, "serve")

        self.debugResourcePath = os.path.join(
            SCRIPT_DIR, "serve", self.settings["mediaDir"]
        )

        self.images = {}

        self.videos = {}

        self.audio = {}

        self.gltf = {}

        self.folderPathList = {}

        self.mdPathList = {}

        self.mdFileList = {}

        self.gatherMedia()

        if os.path.isdir(self.resourcePath):

            self.resourcesExist = True

        if os.path.isfile(self.dataFilePath):

            dataFile = open(self.dataFilePath, "rb")

            data = pickle.load(dataFile)

            if self.settings["siteName"] != "" or self.settings["siteName"] != "dist":

                self.distPath = self.distPath.replace("dist", self.settings["siteName"])

            self.pageList = data["pageList"]

            self.folders = data["folders"]

            self.folderData = data["folderData"]

            self.pageData = data["pageData"]

            self.columnWidths = data["columnWidths"]

            self.articleData = data["articleData"]

            self.articleOrder = data["articleOrder"]

            self.formData = data["formData"]

            self.metaData = data["metaData"]

            # Merge loaded settings with defaults to preserve new features

            loaded_settings = data["settings"]

            for key, value in self.settings.items():

                if key not in loaded_settings:

                    loaded_settings[key] = value

            self.settings = loaded_settings

            # Ensure font settings are properly initialized

            self._ensureFontSettings()

            self.authors = data["authors"]

            self.css_components = self.css_themes[self.settings["theme"]]

            self.fileExists = True

            self.debugResourcePath = os.path.join(
                SCRIPT_DIR, "serve", self.settings["mediaDir"]
            )

            self.images = data["media"]["images"]

            self.videos = data["media"]["videos"]

            self.audio = data["media"]["audio"]

            self.gltf = data["media"]["gltf"]

            self.folderPathList = data["folderPathList"]

            self.mdPathList = data["mdPathList"]

            self.mdFileList = data["mdFileList"]

        if os.path.isfile(self.dataBakFilePath):

            dataFile = open(self.dataBakFilePath, "rb")

            data = pickle.load(dataFile)

            self._old_pageList = data["pageList"]

            self._old_folders = data["folders"]

            self._old_folderData = data["folderData"]

            self._old_pageData = data["pageData"]

            self._old_columnWidths = data["columnWidths"]

            self._old_articleData = data["articleData"]

            self._old_articleOrder = data["articleOrder"]

            self._old_formData = data["formData"]

            self._old_metaData = data["metaData"]

            self._old_settings = data["settings"]

            self._old_authors = data["authors"]

            self._old_css_components = data["css_components"]

            self._old_fileExists = True

            self._old_images = data["media"]["images"]

            self._old_videos = data["media"]["videos"]

            self._old_audio = data["media"]["audio"]

            self._old_gltf = data["media"]["gltf"]

            self._old_folderPathList = data["folderPathList"]

            self._old_mdPathList = data["mdPathList"]

            self._old_mdFileList = data["mdFileList"]

        if not os.path.isdir(self.debugResourcePath):

            print("Create media folder")

            os.makedirs(self.debugResourcePath)

            print(self.debugResourcePath)

            print(os.path.isdir(self.debugResourcePath))

        if not os.path.isfile(self.dataBakFilePath):

            self.keys = Keypair.random()

            self.keys_25519 = Stellar25519KeyPair(self.keys)

            self.pub25519 = self.keys_25519.public_key()

            self.updateSetting("private_key", self.keys.secret)

            self.updateSetting("25519_pub", self.pub25519)

            self.settings["private_key"] = self.keys.secret

            self.firstRun = True

        else:

            self.keys = Keypair.from_secret(self.settings["private_key"])

            self.keys_25519 = Stellar25519KeyPair(self.keys)

            self.pub25519 = self.keys_25519.public_key()

            self.firstRun = False

        home_info = self.detectHomePage()

        if home_info["exists"]:

            self.hasHomePage = True

        else:

            self.hasHomePage = False

        self.deployHandler = W3DeployHandler.W3DeployHandler(
            self.filePath, self.debugPath, self.resourcePath, self.settings
        )

        # Ensure font settings are properly initialized

        self._ensureFontSettings()

        self.saveData()

    def _reorder_list(self, l, list_element, index):

        i = l.index(list_element)

        tmp1 = []

        tmp2 = []

        for a in l:

            tmp1.append(a)

            tmp2.append(a)

        items = deque(tmp1)

        items.rotate(index)

        tmp1 = list(items)

        j = tmp1.index(list_element)

        tmp2.insert(j, tmp2.pop(i))

        return tmp2

    def movePageUp(self, page):

        self.pageList = self._reorder_list(self.pageList, page, -1)

    def movePageDown(self, page):

        self.pageList = self._reorder_list(self.pageList, page, 1)

    def addFolderPath(self, folder, path):

        self.folderPathList[folder] = path

    def updateFolderData(self, folder):

        articleList = []

        for a in self.articleData[folder].keys():

            articleList.append(a)

        self.folderData[folder] = {"articleList": articleList}

    def addMdPath(self, file, path):

        analyzer = MarkdownAnalyzer(path)

        self.mdPathList[file] = path

        self.mdFileList[file] = analyzer.identify_links()

    def renderStaticPage(self, template_file, data):
        """



        Render the static page with media links already replaced.



        First renders to serve folder, then copies to dist folder for deployment.



        """

        # Render to serve folder first

        target_path = os.path.join(SCRIPT_DIR, "serve")

        page_path = os.path.join(target_path, "index.html")

        self.markdownHandler.renderPageTemplate(template_file, data, page_path)

        # Ensure dist folder exists and copy the rendered file there

        if hasattr(self, "distPath") and self.distPath:

            import shutil

            os.makedirs(self.distPath, exist_ok=True)

            dist_index_path = os.path.join(self.distPath, "index.html")

            # Copy the rendered index.html to dist folder

            try:

                shutil.copy2(page_path, dist_index_path)

                print(f"Copied rendered index.html to dist folder: {dist_index_path}")

            except Exception as e:

                print(f"Warning: Could not copy to dist folder: {e}")

        else:

            print("Warning: No distPath configured, cannot copy rendered file")

    def generateFormData(self, page, article):

        result = []

        form_data = self.formData[page][article]

        for k in form_data["formType"].keys():

            if form_data["formType"][k] == True:

                result.append(k)

        return result

    def generatePageData(self, page):

        result = {
            "title": None,
            "icon": None,
            "use_text": True,
            "max_height": None,
            "columns": None,
            "footer_height": None,
            "content": {"columns": [], "widths": self.columnWidths[page]},
        }

        for k in self.pageData[page].keys():

            result[k] = self.pageData[page][k]

        columns = int(self.pageData[page]["columns"])

        for idx in range(0, columns):

            result["content"]["columns"].append([])

        for k in self.folderData[page]["articleList"]:

            article_data = {
                "column": None,
                "type": None,
                "style": None,
                "border": None,
                "max_width": "90",
                "author": None,
                "use_thumb": None,
                "html": None,
                "height": None,
                "author_img": None,
                "bg_img": None,
                "form_data": [],
                "form_html": "",
                "form_btn_txt": "",
                "form_response": "",
                "form_id": "",
                "images": [],
                "videos": [],
                "nft_start_supply": 1024,
                "contract": "",
                "metadata_link": "",
                "metadata": json.dumps(self.opensea_metadata),
                "file_type": None,
            }

            props = self.articleData[page][k].keys()

            for prop in props:

                article_data[prop] = self.articleData[page][k][prop]

            # Debug: Check what HTML content we have

            if "html" in article_data and article_data["html"]:

                print(
                    f"DEBUG: Article '{k}' HTML content preview: {article_data['html'][:200]}..."
                )

                # Check if it contains media links

                media_dir = self.settings.get("mediaDir", "_resources")

                if f"../{media_dir}/" in article_data["html"]:

                    print(f"DEBUG: Article '{k}' still contains local media links!")

                else:

                    print(
                        f"DEBUG: Article '{k}' HTML appears to have media links replaced"
                    )

            author = self.articleData[page][k]["author"]

            author_img = self.authors[author]

            article_data["author_img"] = author_img

            if article_data["type"] == "Form":

                article_data["form_data"] = self.generateFormData(page, k)

                article_data["form_html"] = self.formData[page][k]["customHtml"]

                article_data["form_btn_txt"] = self.formData[page][k]["btn_txt"]

                article_data["form_response"] = self.formData[page][k]["response"]

                article_data["form_id"] = self.formData[page][k]["form_id"]

            index = int(article_data["column"]) - 1

            result["content"]["columns"][index].append(article_data)

        return result

    def generateSiteData(self):

        result = {"pages": [], "settings": self.settings}

        # Check for home page first (READ-ONLY operation)

        home_info = self.detectHomePage()

        if home_info["exists"]:

            self.hasHomePage = True

            # Generate home page data without touching existing structures

            result["homePage"] = self.generateHomePageData(home_info)

            result["hasHomePage"] = True

        else:

            self.hasHomePage = False

            result["hasHomePage"] = False

        # Generate regular page data (existing logic unchanged)

        for page in self.pageList:

            page_data = self.generatePageData(page)

            result["pages"].append(page_data)

        return result

    def detectHomePage(self):
        """Detect if a home page exists and return its configuration







        IMPORTANT: Home page detection ONLY looks in the base project folder (self.filePath),



        NOT in subfolders. This ensures home pages are project-level landing pages.







        Example project structure:



        project/



        ├── section1/



        │   ├── hello.md



        │   └── Info.md



        ├── section2/



        │   ├── About.md



        │   ├── Tutorial1.md



        │   └── Tutorial2.md



        ├── _resources/



        │   ├── hello.png



        │   └── cat.jpg



        └── home.md  ← This is detected as the home page



        """

        home_candidates = ["home.md", "index.md", "landing.md", "welcome.md"]

        # CRITICAL: Only check in base project folder, not subfolders

        for candidate in home_candidates:

            candidate_path = os.path.join(self.filePath, candidate)

            if os.path.exists(candidate_path):

                return {
                    "exists": True,
                    "filename": candidate,
                    "path": candidate_path,
                    "type": "markdown",
                    "location": "base_folder",
                }

        return {"exists": False, "type": "none", "location": "none"}

    def isHomePageEnabled(self):
        """Check if home page functionality is enabled"""

        return self.detectHomePage()["exists"]

    def validateHomePageLocation(self, file_path):
        """Validate that a potential home page is in the correct location







        Args:



            file_path (str): Path to the file to validate







        Returns:



            bool: True if file is in base project folder, False otherwise



        """

        # Ensure the file is directly in the base project folder

        file_dir = os.path.dirname(file_path)

        return os.path.abspath(file_dir) == os.path.abspath(self.filePath)

    def extractFrontmatter(self, markdown_content):
        """Extract YAML frontmatter from markdown content"""

        import re

        import yaml

        # Pattern for YAML frontmatter: --- at start and end

        frontmatter_pattern = r"^---\s*\n(.*?)\n---\s*\n"

        match = re.match(frontmatter_pattern, markdown_content, re.DOTALL)

        if match:

            try:

                frontmatter = yaml.safe_load(match.group(1))

                content = markdown_content[match.end() :]

                return frontmatter, content

            except yaml.YAMLError as e:

                print(f"Warning: Invalid frontmatter in home page: {e}")

                return {}, markdown_content

        return {}, markdown_content

    def generateHomePageData(self, home_info):
        """Generate home page data from markdown file"""

        try:

            with open(home_info["path"], "r", encoding="utf-8") as f:

                markdown_content = f.read()

            # Extract frontmatter and content

            frontmatter, content = self.extractFrontmatter(markdown_content)

            # Convert to HTML (will include frontmatter, we'll filter it out)

            html_content = self.markdownHandler.generateHTML(home_info["path"])

            # Remove frontmatter from HTML if it exists

            # The MarkdownHandler processes the entire file, so we need to filter out the frontmatter

            # Look for the start of actual content (after the frontmatter)

            if "<h1>" in html_content:

                # Find the first <h1> tag and start from there

                h1_start = html_content.find("<h1>")

                html_content = html_content[h1_start:]

            elif "<h2>" in html_content:

                # Fallback to <h2> if no <h1>

                h2_start = html_content.find("<h2>")

                html_content = html_content[h2_start:]

            # Process the HTML content for navigation links (convert regular links to nav-links)

            processed_html = self.processHomePageContentHTML(html_content)

            # Apply navigation link processing to HTML

            final_html = self.processHomePageNavigation(processed_html)

            return {
                "type": "home",
                "title": frontmatter.get("title", "Home"),
                "description": frontmatter.get("description", ""),
                "layout": frontmatter.get("layout", "hero"),
                "content": {
                    "markdown": content,
                    "html": final_html,
                    "hero_title": frontmatter.get("hero_title", ""),
                    "hero_subtitle": frontmatter.get("hero_subtitle", ""),
                    "hero_image": frontmatter.get("hero_image", ""),
                    "cta_button": frontmatter.get("cta_button", {}),
                },
                "navigation": frontmatter.get("navigation", []),
                "seo": frontmatter.get("seo", {}),
                "source": "markdown",
                "filename": home_info["filename"],
            }

        except Exception as e:

            print(f"Error generating home page data: {e}")

            return None

    def processHomePageContent(self, markdown_content):
        """Process markdown content for navigation links"""

        import re

        # Pattern for links that might be page references

        link_pattern = r"\[([^\]]+)\]\(([^)]+)\)"

        def process_link(match):

            text = match.group(1)

            href = match.group(2)

            # Check if this looks like a page reference

            if self._isPageReference(href):

                # Mark for special processing (we'll handle this in HTML)

                return f'<a href="#nav:{href}" class="nav-link" data-page="{href}">{text}</a>'

            else:

                # Keep as regular markdown link

                return match.group(0)

        return re.sub(link_pattern, process_link, markdown_content)

    def processHomePageContentHTML(self, html_content):
        """Process HTML content to convert regular links to navigation links"""

        import re

        # Pattern for HTML links that might be page references

        link_pattern = r'<a href="([^"]+)">([^<]+)</a>'

        def process_link(match):

            href = match.group(1)

            text = match.group(2)

            # Check if this looks like a page reference

            if self._isPageReference(href):

                # Convert to navigation link format

                return f'<a href="#nav:{href}" class="nav-link" data-page="{href}">{text}</a>'

            else:

                # Keep as regular link

                return match.group(0)

        return re.sub(link_pattern, process_link, html_content)

    def _isPageReference(self, href):
        """Check if href is a reference to a site page.
        
        Args:
            href (str): The href to check, which could be a path or page name
            
        Returns:
            bool: True if the href references a valid page, False otherwise
        """
        if not href or not isinstance(href, str):
            return False

        # Clean and normalize the href
        clean_href = (
            href.lstrip("#/.")
            .replace(".html", "")
            .replace(".md", "")
            .lower()
            .strip()
        )

        # Skip empty or non-page references (like external URLs)
        if not clean_href or clean_href.startswith(('http://', 'https://', 'mailto:', 'tel:')):
            return False

        # Check against existing pages in pageList (case-insensitive)
        return any(page.lower() == clean_href for page in self.pageList if page and isinstance(page, str))

    def processHomePageNavigation(self, html_content):
        """Process HTML content to convert navigation links to functional buttons"""

        soup = BeautifulSoup(html_content, "html.parser")

        # Find all navigation links

        nav_links = soup.find_all("a", class_="nav-link")

        for link in nav_links:

            page_name = link.get("data-page", "")

            if page_name and page_name in self.pageList:

                # Create Onsen UI button with correct navigation type

                button = self._createNavigationButton(
                    link, page_name, self.settings["pageType"]
                )

                link.replace_with(button)

        return str(soup)

    def _createNavigationButton(self, link_element, page_name, navigation_type):
        """Create a functional navigation button from a link"""

        # Extract text and styling from original link

        text = link_element.get_text()

        classes = link_element.get("class", [])

        # Determine button style based on classes or default to primary

        button_style = "primary"

        if "secondary" in classes:

            button_style = "secondary"

        elif "outline" in classes:

            button_style = "outline"

        # Generate correct navigation function based on navigation type

        if navigation_type == "tabs":

            onclick_function = f"fn.goToTabByName('{page_name}')"

        elif navigation_type == "carousel":

            onclick_function = f"fn.goToPageByName('{page_name}')"

        else:  # splitter mode (default)

            onclick_function = f"fn.load('{page_name}.html')"

        # Create Onsen UI button with navigation

        button_html = f"""
       <ons-button onclick="{onclick_function}" modifier="{button_style}" class="home-nav-button">
           {text}
       </ons-button>
       """

        return BeautifulSoup(button_html, "html.parser").find("ons-button")

    def _createNavigationButtonEnhanced(self, link_element, page_name, navigation_type):
        """Create a functional navigation button with enhanced styling"""

        # Extract text and styling from original link

        text = link_element.get_text()

        classes = link_element.get("class", [])

        # Enhanced button style detection

        button_style = "primary"

        button_size = "default"

        if "secondary" in classes:

            button_style = "secondary"

        elif "outline" in classes:

            button_style = "outline"

        elif "quiet" in classes:

            button_style = "quiet"

        if "large" in classes:

            button_size = "large"

        elif "small" in classes:

            button_size = "small"

        # Generate correct navigation function based on navigation type

        if navigation_type == "tabs":

            onclick_function = f"fn.goToTabByName('{page_name}')"

        elif navigation_type == "carousel":

            onclick_function = f"fn.goToPageByName('{page_name}')"

        else:  # splitter mode (default)

            onclick_function = f"fn.load('{page_name}.html')"

        # Create button with size and style

        button_html = f"""



       <ons-button onclick="{onclick_function}" modifier="{button_style}" size="{button_size}" class="home-nav-button">



           {text}



       </ons-button>



       """

        return BeautifulSoup(button_html, "html.parser").find("ons-button")

    def processHomePageNavigationEnhanced(self, html_content):
        """Process HTML content with fallback handling"""

        soup = BeautifulSoup(html_content, "html.parser")

        # Find all navigation links

        nav_links = soup.find_all("a", class_="nav-link")

        for link in nav_links:

            page_name = link.get("data-page", "")

            if page_name and page_name in self.pageList:

                # Create functional button with correct navigation type

                button = self._createNavigationButtonEnhanced(
                    link, page_name, self.settings["pageType"]
                )

                link.replace_with(button)

            else:

                # Fallback: convert to regular link with warning

                if page_name:

                    print(
                        f"Warning: Page '{page_name}' not found, keeping as regular link"
                    )

                    link["href"] = f"#{page_name}"

                    link["class"] = ["nav-link", "nav-link-fallback"]

        return str(soup)

    def safeDataUpdate(self, operation_name, update_function, *args, **kwargs):
        """Safely execute data updates with rollback capability"""

        # Create backup of current state

        backup_state = self._createDataBackup()

        try:

            # Execute the update

            result = update_function(*args, **kwargs)

            # Validate data consistency

            if not self._validateDataConsistency():

                raise ValueError(
                    f"Data consistency check failed after {operation_name}"
                )

            # Log successful update

            print(f"SUCCESS: {operation_name} completed successfully")

            return result

        except Exception as e:

            # Rollback on failure

            print(f"ERROR: {operation_name} failed, rolling back: {e}")

            self._restoreDataBackup(backup_state)

            raise

    def _createDataBackup(self):
        """Create a backup of critical data structures"""

        return {
            "pageList": self.pageList.copy(),
            "articleData": self.articleData.copy(),
            "folderData": self.folderData.copy(),
            "folderPathList": self.folderPathList.copy(),
            "mdPathList": self.mdPathList.copy(),
        }

    def _restoreDataBackup(self, backup_state):
        """Restore data structures from backup"""

        self.pageList = backup_state["pageList"]

        self.articleData = backup_state["articleData"]

        self.folderData = backup_state["folderData"]

        self.folderPathList = backup_state["folderPathList"]

        self.mdPathList = backup_state["mdPathList"]

        print("Data structures restored from backup")

    def _validateDataConsistency(self):
        """Validate that data structures are consistent"""

        try:

            # Check that all pages in pageList have corresponding data

            for page in self.pageList:

                if page not in self.folderPathList:

                    print(f"WARNING: Page '{page}' missing from folderPathList")

                    return False

                if page not in self.folderData:

                    print(f"WARNING: Page '{page}' missing from folderData")

                    return False

            # Check that folderData and articleData are consistent

            for page in self.folderData:

                if page not in self.pageList:

                    print(f"WARNING: Folder '{page}' in folderData but not in pageList")

                    return False

            return True

        except Exception as e:

            print(f"ERROR: Data consistency check failed: {e}")

            return False

    def baseFolder(self, f_path):

        sep = os.path.sep

        arr = f_path.split(sep)

        return arr[len(arr) - 2]

    def addFolder(self, folder, selfData):

        result = False

        if folder not in selfData:

            selfData[folder] = {}

            result = True

        return result

    def addPageAll(self, folder):

        result = False

        if self.addFolder(folder, self.pageData):

            result = True

        if self.addFolder(folder, self.columnWidths):

            result = True

        return result

    def addFolderAll(self, folder):

        result = False

        if self.addFolder(folder, self.folders):

            result = True

        if self.addFolder(folder, self.pageData):

            result = True

        if self.addFolder(folder, self.columnWidths):

            result = True

        if self.addFolder(folder, self.articleData):

            result = True

        if self.addFolder(folder, self.formData):

            result = True

        if self.addFolder(folder, self.metaData):

            result = True

        return result

    def hasNoFolder(self, folder):

        result = False

        if folder not in self.pageData.keys():

            result = True

        return result

    def hasNoFileFolder(self, folder):

        result = False

        if folder not in self.folders:

            result = True

        if folder not in self.articleData:

            result = True

        if folder not in self.formData:

            result = True

        if folder not in self.metaData:

            result = True

        return result

    def hasNoFile(self, folder, path):

        result = False

        if path not in self.folders[folder]:

            result = True

        if path not in self.articleData[folder]:

            result = True

        if path not in self.formData[folder]:

            result = True

        if path not in self.metaData[folder]:

            result = True

        return result

    def pruneFiles(self):

        if not self.firstRun:

            for k, path in self._old_mdPathList.items():

                if not os.path.isfile(path):

                    f_name = os.path.basename(path)

                    basepath = path.replace(f_name, "")

                    f_path = self.baseFolder(basepath)

                    self.oldDataFolders.append(f_path)

                    self.oldDataKeys.append(f_name)

                    print(f_path + " is added to old folders")

                    print(f_name + " is added to old data keys")

                    for f, obj in self._old_mdFileList[k].items():

                        print(obj)

    def pruneFolders(self):

        if not self.firstRun:

            for k, path in self._old_folderPathList.items():

                if not os.path.isdir(path):

                    self.oldFolders.append(k)

                    print(k + " is added to old folders")

    def deleteFolder(self, folder, selfData):

        if folder in selfData.keys():

            selfData.pop(folder)

            print("deleting folder: " + folder)

    def deleteFile(self, folder, path, selfData):

        if folder in selfData.keys() and path in selfData[folder].keys():

            print("deleting: " + path + " from " + folder)

            selfData[folder].pop(path)

    def cloneDirectory(self, source, target):

        if os.path.isdir(source) and os.path.isdir(target):

            source_files = os.listdir(source)

            target_files = os.listdir(target)

            for f in target_files:

                f_path = os.path.join(target, f)

                os.remove(f_path)

            for f in source_files:

                src_path = os.path.join(source, f)

                dst_path = os.path.join(target, f)

                shutil.copy(src_path, dst_path)

    def convertVideos(self, folder):

        if shutil.which("ffmpeg") == False:

            return

        files = os.listdir(folder)

        for f in files:

            if ".mp4" in f:

                print(f)

                in_file = os.path.join(folder, f)

                out_file = in_file.replace(".mp4", "_$$$.mp4")

                if os.path.isfile(in_file):

                    ff = ffmpy.FFmpeg(
                        inputs={in_file: None},
                        outputs={out_file: "-brand mp42 -pix_fmt yuv420p -y"},
                    )

                    ff.run()

                    os.remove(in_file)

                    os.rename(out_file, in_file)

    def setCss(self, theme):

        self.css_components = self.css_themes[theme]

        self.settings["css_components"] = self.css_components

        self.settings["theme"] = theme

        self.saveData()

    def resetCss(self):

        self.settings["css_components"] = self.css_components

        self.saveData()

    def refreshCss(self):

        if os.path.isfile(self.settings["customTheme"]):

            file = os.path.basename(self.settings["customTheme"])

            if "theme.css" in file:

                with open(self.settings["customTheme"], "r") as f:

                    txt = ""

                    line = f.readline()

                    while line:

                        txt += line

                        line = f.readline()

                    arr = txt.split("{")[1].split("}")

                    css = arr[0]

                    self.settings["css_components"] = css

                    self.saveData()

            else:

                print("Invalid Css file")

        else:

            print("Invalid Css file")

    def deleteDist(self):

        print("deleteDist")

        siteName = self.settings["siteName"]

        dist = os.path.basename(os.path.normpath(self.distPath))

        if (siteName != "" and siteName not in self.distPath) or dist != siteName:

            self.distPath = self.distPath.replace(dist, self.settings["siteName"])

        if self.distPath != SCRIPT_DIR and os.path.isdir(self.distPath):

            target_files = os.listdir(self.distPath)

            for f in target_files:

                f_path = os.path.join(self.distPath, f)

                if os.path.isfile(f_path) and self.distPath != SCRIPT_DIR:

                    os.remove(f_path)

            shutil.rmtree(self.distPath)

    def refereshDist(self):

        self.deleteDist()

        shutil.copytree(self.debugPath, self.distPath)

    def refreshDebugMedia(self):

        self.cloneDirectory(self.resourcePath, self.debugResourcePath)

        self.convertVideos(self.debugResourcePath)

    def deleteOldFiles(self):

        idx = 0

        for folder in self.oldDataFolders:

            path = self.oldDataKeys[idx]

            self.deleteFile(folder, path, self.folders)

            self.deleteFile(folder, path, self.articleData)

            self.deleteFile(folder, path, self.formData)

            self.deleteFile(folder, path, self.metaData)

            self.deleteFile(folder, path, self.pageData)

            if (
                folder in self.folderData
                and path in self.folderData[folder]["articleList"]
            ):

                self.folderData[folder]["articleList"].pop(
                    self.folderData[folder]["articleList"].index(path)
                )

        for folder in self.oldFolders:

            self.deleteFolder(folder, self.folderData)

            self.deleteFolder(folder, self.folders)

            self.deleteFolder(folder, self.pageData)

            self.deleteFolder(folder, self.columnWidths)

            self.deleteFolder(folder, self.articleData)

            self.deleteFolder(folder, self.formData)

            self.deleteFolder(folder, self.metaData)

            # CRITICAL FIX: Also remove from pageList and folderPathList

            if folder in self.pageList:

                self.pageList.remove(folder)

                print(f"Removed deleted folder '{folder}' from pageList")

            if folder in self.folderPathList:

                self.folderPathList.pop(folder, None)

                print(f"Removed deleted folder '{folder}' from folderPathList")

        self.oldDataFolders.clear()

        self.oldDataKeys.clear()

        self.oldFolders.clear()

    def mediaSaved(self, file_name):

        result = False

        if (
            file_name in self.images.keys()
            or file_name in self.videos.keys()
            or file_name in self.audio.keys()
            or file_name in self.gltf.keys()
        ):

            result = True

        return result

    def mediaOutOfDate(self, file_name, m_type):

        result = False

        media = {
            "images": self.images,
            "videos": self.videos,
            "audio": self.audio,
            "gltf": self.gltf,
        }

        if file_name in media[m_type].keys():

            path = media[m_type][file_name]["path"]

            time_stamp = media[m_type][file_name]["time_stamp"]

            if self.fileIsNew(path, time_stamp):

                result = True

        return result

    def fileList(self, ext):

        result = {}

        if os.path.isdir(self.resourcePath):

            media = {
                "images": self.images,
                "videos": self.videos,
                "audio": self.audio,
                "gltf": self.gltf,
            }

            files = os.listdir(self.resourcePath)

            m_type = "image"

            if ext == ".mp4":

                m_type = "video"

            elif ext == ".mp3":

                m_type = "audio"

            elif ext == ".gltf":

                m_type = "3d"

            for f in files:

                f_path = os.path.join(self.resourcePath, f)

                t_stamp = time.strftime(
                    "%b %d %H:%M:%S %Y", time.gmtime(os.path.getmtime(f_path))
                )

                obj = {
                    "type": m_type,
                    "path": f_path,
                    "cid": None,
                    "time_stamp": t_stamp,
                }

                key = "images"

                if m_type == "video":

                    key = "videos"

                elif m_type == "audio":

                    key = "audio"

                elif m_type == "3d":

                    key = "gltf"

                if os.path.isfile(f_path) and ext in f:

                    if (
                        self.mediaSaved(f) == False
                        or self.mediaOutOfDate(f, key) == True
                    ):

                        result[f] = obj

                    else:

                        if m_type == "image":

                            result[f] = media["images"][f]

                        elif m_type == "video":

                            result[f] = media["videos"][f]

                        elif m_type == "audio":

                            result[f] = media["audio"][f]

                        elif m_type == "3d":

                            result[f] = media["gltf"][f]

        return result

    def fileIsNew(self, filePath, time_stamp):

        result = False

        t = time.strftime("%b %d %H:%M:%S %Y", time.gmtime(os.path.getmtime(filePath)))

        latest = max((t, time_stamp))

        if t == latest and t != time_stamp:

            result = True

        return result

    def setDeployFolder(self, folder):

        self.deployHandler.deployFolderName = folder

    def deployMedia(self, usefullPath=False, askPermission=True):
        """



        Deploy all media files from the media folder.



        Returns a tuple (media_cid, status) for backward compatibility.



        """

        try:

            result = False

            deployFolder = self.resourcePath

            self.refreshDebugMedia()

            if (
                os.path.isdir(self.debugResourcePath)
                and len(os.listdir(self.debugResourcePath)) > 0
            ):

                deployFolder = self.debugResourcePath

            if self.deployHandler.manifest != None:

                self.markdownHandler.deployerManifest = self.deployHandler.manifest

            # Use the new simplified media upload method

            media_manifest = self.deployHandler.uploadMediaFiles(deployFolder)

            self.deployHandler.saveData()

            # For backward compatibility, return a tuple

            if media_manifest:

                # Return first media file's CID and a status message

                first_file = next(iter(media_manifest.values()))

                return (first_file["cid"], "media_deployed")

            return (None, None)

        except Exception as e:

            print(f"Error deploying media: {e}")

            return (None, None)

    def deploySite(self, usefullPath=False, askPermission=True):
        """



        Deploy the built site to IPFS.



        Returns a tuple of (cid, url) or (None, None) on failure.



        """

        try:

            # Validate that we have a distribution path

            if not hasattr(self, "distPath") or not self.distPath:

                print("Error: No distribution path configured")

                return (None, None)

            if not os.path.exists(self.distPath):

                print(f"Error: Distribution directory does not exist: {self.distPath}")

                return (None, None)

            if not os.path.isdir(self.distPath):

                print(f"Error: Distribution path is not a directory: {self.distPath}")

                return (None, None)

            if self.deployHandler.manifest != None:

                self.markdownHandler.deployerManifest = self.deployHandler.manifest

            # Use the new simplified site deployment method

            result = self.deployHandler.deploySite(self.distPath)

            self.deployHandler.saveData()

            return result

        except Exception as e:

            print(f"Error: Site deployment failed: {e}")

            return (None, None)

    def gatherMedia(self):

        self.images = self.fileList(".png")

        self.videos = self.fileList(".mp4")

        self.audio = self.fileList(".mp3")

        self.gltfs = self.fileList(".gltf")

        return {
            "images": self.images,
            "videos": self.videos,
            "audio": self.audio,
            "gltf": self.gltf,
        }

    def updateData(self, folder, path, selfData, data):

        if folder in selfData:

            selfData[folder][path] = data

        else:

            self.addFolder(folder, self.folders)

            self.updateData(folder, path, selfData, data)

    def updateFile(self, folder, path, uiType, active=True):

        if folder in self.folders:

            data = {"path": path, "type": uiType, "active": active}

            self.updateData(folder, path, self.folders, data)

        else:

            self.addFolder(folder, self.folders)

            self.updateFile(folder, path, uiType, active)

    def updatePageData(self, folder, data):

        if folder in self.pageData:

            self.pageData[folder] = data

        else:

            self.addFolder(folder, self.pageData)

            self.updatePageData(folder, data)

    def updateColumnWidths(self, folder, data):

        if folder in self.columnWidths:

            self.columnWidths[folder] = data

        else:

            self.addFolder(folder, self.columnWidths)

            self.updateColumnWidths(folder, data)

    def moveArticleUp(self, page, article):

        self.folderData[page]["articleList"] = self._reorder_list(
            self.folderData[page]["articleList"], article, -1
        )

    def moveArticleDown(self, page, article):

        self.folderData[page]["articleList"] = self._reorder_list(
            self.folderData[page]["articleList"], article, 1
        )

    def updateArticleData(self, folder, path, data):

        if folder in self.articleData:

            self.updateData(folder, path, self.articleData, data)

        else:

            self.addFolder(folder, self.articleData)

            self.updateArticleData(folder, path, data)

    def updateArticleHTML(self, folder, path, filePath):

        if folder in self.articleData:

            t = time.strftime(
                "%b %d %H:%M:%S %Y", time.gmtime(os.path.getmtime(filePath))
            )

            if self.deployHandler.manifest != None:

                self.markdownHandler.deployerManifest = self.deployHandler.manifest

            self.articleData[folder][path]["html"] = self.markdownHandler.generateHTML(
                filePath
            )

            self.articleData[folder][path]["time_stamp"] = t

    def updateAllArticleHTML(self, folder):

        files = os.listdir(folder)

        for f in files:

            fullname = os.path.join(folder, f)

            f_name = os.path.basename(f)

            f_path = self.baseFolder(fullname.replace(f_name, ""))

            if os.path.isdir(fullname):

                self.updateAllArticleHTML(fullname)

            else:

                self.updateArticleHTML(f_path, f_name, fullname)

    def updateMediaFiles(self, folder, path, filePath):

        if folder in self.articleData:

            html = self.articleData[folder][path]["html"]

            media = self.gatherMedia()

            soup = BeautifulSoup(html, "html.parser")

            html_imgs = soup.find_all("img")

            html_vids = soup.find_all("video")

            for image in media["images"]:

                i_name = os.path.basename(image)

                # TODO: Complete implementation for media file updates

    def updateFormData(self, folder, path, data):

        if folder in self.formData:

            self.updateData(folder, path, self.formData, data)

        else:

            self.addFolder(folder, self.formData)

            self.updateFormData(folder, path, data)

    def updateMetaData(self, folder, path, data):

        if folder in self.metaData:

            self.updateData(folder, path, self.metaData, data)

        else:

            self.addFolder(folder, self.metaData)

            self.updateMetaData(folder, path, data)

    def updateSetting(self, setting, value):

        self.settings[setting] = value

        self.saveData()

    def getData(self, folder, path, selfData):

        result = None

        if folder in selfData.keys() and path in selfData[folder].keys():

            result = selfData[folder][path]

        return result

    def addAuthor(self, name, img):

        if name not in self.authors.keys():

            self.authors[name] = img

    def updateAuthor(self, name, img):

        if name in self.authors.keys():

            self.authors[name] = img

    def deleteAuthor(self, author):

        for page in self.pageList:

            for k in self.articleData[page]:

                if self.articleData[page][k]["author"] == author:

                    self.articleData["author"] = "anonymous"

    def getJsonData(self):

        dataFile = open(self.dataFilePath, "rb")

        data = pickle.load(dataFile)

        json_obj = jsonpickle.encode(data)

        print(json_obj)

    def saveData(self):

        file = open(self.dataFilePath, "wb")

        data = {
            "pageList": self.pageList,
            "folders": self.folders,
            "folderData": self.folderData,
            "pageData": self.pageData,
            "columnWidths": self.columnWidths,
            "articleData": self.articleData,
            "articleOrder": self.articleOrder,
            "formData": self.formData,
            "metaData": self.metaData,
            "settings": self.settings,
            "authors": self.authors,
            "css_components": self.css_components,
            "media": self.gatherMedia(),
            "folderPathList": self.folderPathList,
            "mdPathList": self.mdPathList,
            "mdFileList": self.mdFileList,
        }

        pickle.dump(data, file)

        file.close()

    def onCloseData(self):

        shutil.copy(self.dataFilePath, self.dataBakFilePath)

    def _ensureFontSettings(self):
        """Ensure font settings are properly initialized"""

        if "customFonts" not in self.settings:

            self.settings["customFonts"] = {
                "primary": {
                    "family": "Roboto",
                    "source": "google",
                    "weights": [300, 400, 500, 700],
                    "fallback": "Arial, sans-serif",
                },
                "heading": {
                    "family": "Montserrat",
                    "source": "google",
                    "weights": [400, 600, 700],
                    "fallback": "Helvetica, Arial, sans-serif",
                },
            }

        if "fontSettings" not in self.settings:

            self.settings["fontSettings"] = {
                "enableCustomFonts": True,
                "fontDisplay": "swap",
            }

    # Font management methods

    def getAvailableFonts(self):
        """Return categorized list of available fonts"""

        return self.popular_google_fonts

    def getFontCategories(self):
        """Return font category names"""

        return list(self.popular_google_fonts.keys())

    def getFontsInCategory(self, category):
        """Return fonts in specific category"""

        return self.popular_google_fonts.get(category, [])

    def getFontSettings(self):
        """Get font settings safely"""

        self._ensureFontSettings()

        return self.settings.get("fontSettings", {})

    def getCustomFonts(self):
        """Get custom fonts safely"""

        self._ensureFontSettings()

        return self.settings.get("customFonts", {})

    def resetFontSettings(self):
        """Reset font settings to defaults"""

        self.settings["customFonts"] = {
            "primary": {
                "family": "Roboto",
                "source": "google",
                "weights": [300, 400, 500, 700],
                "fallback": "Arial, sans-serif",
            },
            "heading": {
                "family": "Montserrat",
                "source": "google",
                "weights": [400, 600, 700],
                "fallback": "Helvetica, Arial, sans-serif",
            },
        }

        self.settings["fontSettings"] = {
            "enableCustomFonts": True,
            "fontDisplay": "swap",
        }

        self.saveData()

    def validateFontSettings(self):
        """Validate that font settings are complete and valid"""

        self._ensureFontSettings()

        # Check if all required keys exist

        required_font_keys = ["family", "source", "weights", "fallback"]

        required_settings_keys = ["enableCustomFonts", "fontDisplay"]

        for font_type in ["primary", "heading"]:

            if font_type not in self.settings["customFonts"]:

                return False

            for key in required_font_keys:

                if key not in self.settings["customFonts"][font_type]:

                    return False

        for key in required_settings_keys:

            if key not in self.settings["fontSettings"]:

                return False

        return True

    def getFontSetting(self, key, default=None):
        """Get a specific font setting with default fallback"""

        self._ensureFontSettings()

        return self.settings.get("fontSettings", {}).get(key, default)

    def getCustomFont(self, font_type, key, default=None):
        """Get a specific custom font setting with default fallback"""

        self._ensureFontSettings()

        return self.settings.get("customFonts", {}).get(font_type, {}).get(key, default)

    def areCustomFontsEnabled(self):
        """Check if custom fonts are enabled"""

        return self.getFontSetting("enableCustomFonts", False)

    def getFontDisplay(self):
        """Get font display setting"""

        return self.getFontSetting("fontDisplay", "swap")

    def getFontFamily(self, font_type):
        """Get font family for specific type (primary, heading)"""

        return self.getCustomFont(font_type, "family", "Arial")

    def getFontWeights(self, font_type):
        """Get font weights for specific type (primary, heading)"""

        return self.getCustomFont(font_type, "weights", [400])

    def getFontFallback(self, font_type):
        """Get font fallback for specific type (primary, heading)"""

        return self.getCustomFont(font_type, "fallback", "sans-serif")

    def isGoogleFont(self, font_type):
        """Check if a font type is using Google Fonts"""

        return self.getCustomFont(font_type, "source", "") == "google"

    def getGoogleFontsCSS(self):
        """Get Google Fonts CSS links for enabled fonts"""

        if not self.areCustomFontsEnabled():

            return []

        css_links = []

        font_display = self.getFontDisplay()

        # Primary font

        if self.isGoogleFont("primary"):

            primary_family = self.getFontFamily("primary")

            if primary_family:

                css_links.append(
                    f"https://fonts.googleapis.com/css2?family={primary_family.replace(' ', '+')}:wght@300;400;500;700&display={font_display}"
                )

        # Heading font

        if self.isGoogleFont("heading"):

            heading_family = self.getFontFamily("heading")

            if heading_family:

                css_links.append(
                    f"https://fonts.googleapis.com/css2?family={heading_family.replace(' ', '+')}:wght@400;600;700&display={font_display}"
                )

        return css_links

    def getFontCSSVariables(self):
        """Get CSS variables for font application"""

        if not self.areCustomFontsEnabled():

            return {
                "--font-primary": "Arial, sans-serif",
                "--font-heading": "Helvetica, Arial, sans-serif",
            }

        return {
            "--font-primary": f"'{self.getFontFamily('primary')}', {self.getFontFallback('primary')}",
            "--font-heading": f"'{self.getFontFamily('heading')}', {self.getFontFallback('heading')}",
        }

    def getSafeFontSettings(self):
        """Get font settings with safe defaults for template rendering"""

        self._ensureFontSettings()

        return {
            "fontSettings": {
                "enableCustomFonts": self.settings.get("fontSettings", {}).get(
                    "enableCustomFonts", False
                ),
                "fontDisplay": self.settings.get("fontSettings", {}).get(
                    "fontDisplay", "swap"
                ),
            },
            "customFonts": {
                "primary": {
                    "family": self.settings.get("customFonts", {})
                    .get("primary", {})
                    .get("family", "Roboto"),
                    "source": self.settings.get("customFonts", {})
                    .get("primary", {})
                    .get("source", "google"),
                    "weights": self.settings.get("customFonts", {})
                    .get("primary", {})
                    .get("weights", [300, 400, 500, 700]),
                    "fallback": self.settings.get("customFonts", {})
                    .get("primary", {})
                    .get("fallback", "Arial, sans-serif"),
                },
                "heading": {
                    "family": self.settings.get("customFonts", {})
                    .get("heading", {})
                    .get("family", "Montserrat"),
                    "source": self.settings.get("customFonts", {})
                    .get("heading", {})
                    .get("source", "google"),
                    "weights": self.settings.get("customFonts", {})
                    .get("heading", {})
                    .get("weights", [400, 600, 700]),
                    "fallback": self.settings.get("customFonts", {})
                    .get("heading", {})
                    .get("fallback", "Helvetica, Arial, sans-serif"),
                },
            },
        }

    def getTemplateFontData(self):
        """Get font data formatted for template rendering with safe defaults"""

        return self.getSafeFontSettings()

    def validateFont(self, font_name):
        """Check if font is in our curated list"""

        for category in self.popular_google_fonts.values():

            if font_name in category:

                return True

        return False

    def setFont(self, font_type, font_family, font_weights=None):
        """Set font for specific type (primary, heading)"""

        self.setFontFamily(font_type, font_family)

        if font_weights:

            self.setFontWeights(font_type, font_weights)

    def setFontFamily(self, font_type, font_family):
        """Set font family for specific type (primary, heading)"""

        self.updateCustomFont(font_type, "family", font_family)

    def setFontWeights(self, font_type, font_weights):
        """Set font weights for specific type (primary, heading)"""

        self.updateCustomFont(font_type, "weights", font_weights)

    def setFontSettings(self, enable_custom_fonts, font_display="swap"):
        """Update font settings"""

        self.updateFontSetting("enableCustomFonts", enable_custom_fonts)

        self.updateFontSetting("fontDisplay", font_display)

    def updateFontSetting(self, setting, value):
        """Update a specific font setting using the same pattern as updateSetting"""

        if "fontSettings" in self.settings:

            self.settings["fontSettings"][setting] = value

            self.saveData()

    def updateCustomFont(self, font_type, setting, value):
        """Update a specific custom font setting using the same pattern as updateSetting"""

        if "customFonts" in self.settings and font_type in self.settings["customFonts"]:

            self.settings["customFonts"][font_type][setting] = value

            self.saveData()
