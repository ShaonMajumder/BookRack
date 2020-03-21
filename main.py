import shaonutil
config = shaonutil.file.read_configuration_ini('private/config.ini')
mysql_bin_folder = config['DB']['mysql_bin_folder']
process = shaonutil.process.start_mysql_server(mysql_bin_folder,"private/my.ini")
print(process.pid)
