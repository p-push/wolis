# Wolis - external functional testing for phpBB

## Overview

Wolis is a test suite plus a test runner for phpBB
with a focus on quick test development and low frustration.
You can think of it as phpBB functional tests on steroids.

## Highlights

### Standalone

A key principle of Wolis is it is completely standalone. Unlike phpBB
functional tests which are normally executed within your phpBB repository,
Wolis is designed to be separate from phpBB repository, the tree being tested
and the tree that the web server is using during the actual testing process.
This allows for some interesting operations:

1. Check out a 3.0.11 source tree, copy it to the web root and install a
board. Then copy the tree being tested, which may have uncommitted changes,
over the installed board and run database updater.
2. Install a test board and remove the install directory before running
the remaining tests.
3. Check if the tree being tested cleanly merges into develop or develop-olympus,
even if there are uncommitted changes in the tree. For a branch based on
develop-olympus, check merge first into develop-olympus and then into develop.
4. Merge the tree being tested into develop-olympus, then into develop and
run the test suite.
5. Install an actual extension, which may not be well-behaved, into the
board and run tests.

These operations are not possible in phpBB functional tests because
they cannot modify the tree being tested.

### Rapid development

Despite functional tests existing in phpBB for quite some time, they are
few in quantity and cover rather small amount of functionality. Part of the
reason for this is they take an inordinate amount of time to write.
PHP, having been designed and still very much maintaining a focus on
being an HTML page generator for people with little programming ability,
remains poorly suited for general purpose work like running test suites.
When writing phpBB functional tests, time spent fighting the
environment exceeds time spent actually writing test cases. No more.

Wolis is mostly written in Python, a language much better suited to the task.
Furthermore it uses a test framework ([WebRacer](https://github.com/p/webracer))
specifically designed for
testing full application stacks. All in all developing test cases in
Wolis easily takes an order of magnitude less time and effort than the
corresponding phpBB functional tests would have taken, if they could even
have been written.

### JavaScript testing

Wolis makes use of [CasperJS](http://casperjs.org/)
and [PhantomJS](http://phantomjs.org/) to test the JavaScript code in phpBB.
Currently phpBB's own test suite has no comparable functionality.

### Complete test coverage

With JavaScript testing already implemented, there is nothing impossible for
Wolis as long as it runs on the host machine. In particular, spawning server-side
processes is possible, permitting sphinx search backend to be tested.

Wolis permits every bit of phpBB functionality that is exposed to users
to be tested.

### No fixtures

Wolis does not use fixtures. Tests are run in a known sequence
and data needed by a particular test is created by a previously executed test.

phpBB functional tests are rather confused in this regard: they install
the board once per test run, be that the entire suite or a single test.
As a result, depending on whether a phpBB functional test is run individually
or as part of the full suite it would see different data.

Wolis implements crude resume support for test runs aborted part way.
A comprehensive resume implementation is pending.

### Use of third-party tools

Wolis tries to use existing tools and libraries where practical.
JavaScript testing is performed via CasperJS.
[jshint](http://www.jshint.com/) is employed for JavaScript code checks.
WebRacer, despite being at the core of most of Wolis's tests, is an
independent project. Capybara is being investigated as an alternative way
of testing JavaScript functionality.

The goal of Wolis is to glue these disparate components into a single
coherent system while doing the least possible amount of work.

### Black box testing

For the most part Wolis treats phpBB as a black box, that is, it does not
rely on knowledge of phpBB internals (code or database) beyond the HTML
that phpBB generates.

In practical terms, this means unit tests should still go into phpBB's
test suite.

The one exception where Wolis needs to peek into phpBB's database is
solving captchas. This is intended to be accomplished via a separate
library providing database access in a way that is convenient for test code.

### Multiple database support

Wolis already supports testing phpBB with mysql, mysqli and postgres database
drivers. Support for firebird is planned.

### Multiple phpBB version support

Wolis supports testing both phpBB 3.0 Olympus and phpBB 3.1 Ascraeus from
the same Wolis source tree. Wolis detects automatically which phpBB version
is being tested and adjusts tests accordingly.

### Multi-threading

Tests written in Python can execute code in multiple threads. This is most
handy when performing bulk data inserts. As Wolis primarily drives
other code, workloads that are parallelizable show significant gains when
parallelized. See tests/post_lots.py for an example; this test achieves a
factor of 3 speedup on a two-core system.

## Status

There are still framework features that need to be implemented (in particular,
better resuming functionality) but what is already there is very extensive
and works very well.

Wolis has a lot more tests than phpBB's own functional test suite. Most of
phpBB functional tests are replicated in Wolis. In terms of code coverage
Wolis is greatly ahead of phpBB functional tests.

Wolis can be viewed in action [here](http://integrity.vps.hxr.me/).

## Requirements

- Git
- Python 2.6 or 2.7
- [utu](https://github.com/p/utu)
- [cidict](https://github.com/p/cidict) (WebRacer dependency)
- [ocookie](https://github.com/p/ocookie) (WebRacer dependency)
- [webracer](https://github.com/p/webracer)
- [lxml](http://lxml.de/)
- [yaml](http://pyyaml.org/)
- [Python Imaging Library](http://www.pythonware.com/products/pil/)
- [PhantomJS](http://phantomjs.org/)
- [CasperJS](http://casperjs.org/)
- [Node.js](http://nodejs.org/)
- [coffee-script](http://coffeescript.org/) npm package
- [uglify-js](https://github.com/mishoo/UglifyJS) npm package
- [jshint](http://www.jshint.com/) npm package
- A web server configured to serve PHP
- Write access to a directory under web server's document root
- All PHP extensions needed or optionally usable by phpBB present and enabled
- Your favorite database engine(s) plus client libraries
  - [MySQL-Python](http://mysql-python.sourceforge.net/) for MySQL
  - [psycopg2](http://initd.org/psycopg/) for PostgreSQL
- [Sphinx search](http://sphinxsearch.com/)

Wolis is deployable to a typical Linux VPS.

## Installation

1. Install git if you do not already have it.
2. Install Python using your operating system's package manager.
3. Install [Sphinx](http://sphinxsearch.com/). No configuration is necessary,
but make sure its programs are in PATH.
4. Install virtualenv and pip. If your operating system does not provide
a package for them, follow instructions
[here](http://www.pip-installer.org/en/latest/installing.html).
5. Activate the new environment.
6. Install Python packages: `pip install -r requirements.txt`.
7. [Install PhantomJS.](http://phantomjs.org/download.html)
8. [Install CasperJS.](http://casperjs.org/installation.html)
9. Install node.js. It might be provided by your operating system's package
manager, or follow instructions [here](http://nodejs.org/download/).
10. Install npm. If it did not come with your node.js package, obtain it
from [here](https://github.com/isaacs/npm).
11. Install npm packages: `npm install -g coffee-script uglify-js jshint`.
12. Edit `config/default.yaml`.
13. Configure your web server to serve PHP scripts in `test_root_phpbb`.
14. Configure your web server to serve directory listings in `responses_dir`.
15. Setup sudo access from your user account to the one running PHP scripts,
or arrange for umask/group membership to otherwise give you write access to
files that PHP creates.
16. Choose your database engine and create a database for wolis.

### MySQL stop words

MySQL by default refuses to search for some words that are legitimate,
such as "welcome". In order for wolis to work with mysql, mysql must be told
to not use a stop word list. This can be accomplished via the following entry
in `/etc/my.cnf`:

	[mysqld]
	ft_stopword_file=''

## Usage

To run all tests:

	./script/run

To resume a run that failed partway:

	./script/run -r

To run with a different database driver:

	./script/run -d postgres

To use an alternate configuration file:

	./script/run -c config/special.yaml

Note that `-r` requires all other options to still be passed.

## License

Released under the 2 clause BSD license.
