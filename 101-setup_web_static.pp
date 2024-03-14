# Puppet manifest to setup web static content for AirBnB_clone_v2

# Install nginx package
package { 'nginx':
  ensure => installed,
}

# Ensure nginx service is running and enabled
service { 'nginx':
  ensure  => running,
  enable  => true,
  require => Package['nginx'],
}

# Define the web_static directory structure
file { '/data':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0755',
}

file { '/data/web_static':
  ensure  => directory,
  owner   => 'root',
  group   => 'root',
  mode    => '0755',
}

file { '/data/web_static/releases':
  ensure  => directory,
  owner   => 'root',
  group   => 'root',
  mode    => '0755',
}

file { '/data/web_static/shared':
  ensure  => directory,
  owner   => 'root',
  group   => 'root',
  mode    => '0755',
}

# Create symbolic link for 'current' pointing to 'test'
file { '/data/web_static/current':
  ensure  => link,
  target  => '/data/web_static/releases/test',
  owner   => 'root',
  group   => 'root',
  mode    => '0755',
}

# Create index.html with desired content
file { '/data/web_static/releases/test/index.html':
  ensure  => present,
  content => "<html>\n  <head>\n  </head>\n  <body>\n    Holberton School\n  </body>\n</html>\n",
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0644',
}

# Restart nginx service if there's any change in nginx configuration or content
service { 'nginx':
  ensure  => running,
  enable  => true,
  require => [File['/data/web_static/releases/test/index.html'], Service['nginx']],
}
