from plugins import TestyPluginConfig


class ExamplePluginConfig(TestyPluginConfig):
    name = 'plugin_example'
    verbose_name = 'Plugin example'
    description = 'It is very simple plugin example'
    version = '0.1'
    plugin_base_url = 'plugin-example'
    index_reverse_name = 'upload-file'


config = ExamplePluginConfig
