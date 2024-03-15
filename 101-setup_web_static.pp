# Define a class for setting up web static content
class setup_web_static {
  
  # Create necessary directories
  file { '/data':
    ensure => 'directory',
    owner  => 'ubuntu',
    group  => 'ubuntu',
    mode   => '0755',
  }

  file { '/data/web_static':
    ensure => 'directory',
    owner  => 'ubuntu',
    group  => 'ubuntu',
    mode   => '0755',
  }

  file { '/data/web_static/releases':
    ensure => 'directory',
    owner  => 'root',
    group  => 'root',
    mode   => '0755',
  }

  file { '/data/web_static/shared':
    ensure => 'directory',
    owner  => 'root',
    group  => 'root',
    mode   => '0755',
  }

  # Create symbolic link
  file { '/data/web_static/current':
    ensure => 'link',
    target => '/data/web_static/releases/test',
    owner  => 'root',
    group  => 'root',
  }

  # Create index.html file
  file { '/data/web_static/releases/test/index.html':
    ensure  => 'file',
    owner   => 'root',
    group   => 'root',
    mode    => '0644',
    content => '<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>',
  }
}
