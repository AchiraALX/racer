package { 'postgresql':
    ensure => installed,
}

package { 'redis-server':
    ensure => installed,
}

package { 'libpq-dev':
    ensure => installed,
}
