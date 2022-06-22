from schema import Schema
conf_schema = Schema({
    'connection': {
        'ip': str,
        'port': int,
    },
    'tspi_options': {
        'ttl': int,
    },
    'projection_options': {
        'time_offset': int
    },
    'alert_options': {
        'invalid_data_max_count': int,
        'depth_violation_max_count': int,
        'proj_pos_violation_max_count': int,
    }
})
