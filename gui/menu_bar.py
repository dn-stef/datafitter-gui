import wx

def create_menu_bar(frame):
    menubar = wx.MenuBar()
    
    file_menu = wx.Menu()
    upload_item = file_menu.Append(wx.ID_ANY, 'Upload data file\tCtrl+O')
    output_dir_item = file_menu.Append(wx.ID_ANY, 'Choose output directory\tCtrl+D')
    file_menu.AppendSeparator()
    exit_item = file_menu.Append(wx.ID_ANY, 'Exit\tCtrl+Q')

    plot_menu = wx.Menu()
    fit_result_item = plot_menu.Append(wx.ID_ANY, 'Fit result\tCtrl+P')

    view_menu = wx.Menu()
    small_font_item = view_menu.Append(wx.ID_ANY, 'Set small font size\tCtrl+1')
    medium_font_item = view_menu.Append(wx.ID_ANY, 'Set medium font size\tCtrl+2')
    large_font_item = view_menu.Append(wx.ID_ANY, 'Set large font size\tCtrl+3')

    help_menu = wx.Menu()
    about_item = help_menu.Append(wx.ID_ANY, 'About DataFitter\tCtrl+H')

    menus = {file_menu: 'File',
             plot_menu: 'Plot',
             view_menu: 'View',
             help_menu: 'Help'}
    
    for menu, name in menus.items():
        menubar.Append(menu, name)

    frame.SetMenuBar(menubar)

    frame.Bind(wx.EVT_MENU, lambda e: frame.panel.on_choose_file(e), upload_item)
    frame.Bind(wx.EVT_MENU, lambda e: frame.panel.on_choose_directory(e), output_dir_item)
    frame.Bind(wx.EVT_MENU, lambda e: frame.Close(), exit_item)
    frame.Bind(wx.EVT_MENU, lambda e: frame.panel.on_fit_result(e), fit_result_item)
    frame.Bind(wx.EVT_MENU, lambda e: frame.panel.on_font_change('small'), small_font_item)
    frame.Bind(wx.EVT_MENU, lambda e: frame.panel.on_font_change('medium'), medium_font_item)
    frame.Bind(wx.EVT_MENU, lambda e: frame.panel.on_font_change('large'), large_font_item)
    frame.Bind(wx.EVT_MENU, lambda e: frame.panel.on_about(e), about_item)

    return menubar