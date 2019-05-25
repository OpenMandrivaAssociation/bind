%define Werror_cflags -Wformat
%define _disable_lto 1
# For plugins
%global _disable_ld_no_undefined 1

%define plevel %{nil}

# default options
%define sdb_mysql 0
%bcond_with gssapi

%{?_with_sdb_mysql: %{expand: %%global sdb_mysql 1}}
%{?_without_sdb_mysql: %{expand: %%global sdb_mysql 0}}

Summary:	A DNS (Domain Name System) server
Name:		bind
Epoch:		1
Version:	9.15.0
%if "%plevel" != ""
Release:	0.%{plevel}.1
Source0:	ftp://ftp.isc.org/isc/%{name}9/%{version}-%plevel/%{name}-%{version}-%{plevel}.tar.gz
%else
Release:	1
Source0:	ftp://ftp.isc.org/isc/%{name}9/%{version}/%{name}-%{version}.tar.gz
%endif
License:	Distributable
Group:		System/Servers
Url:		http://www.isc.org/products/BIND/
Source2:	bind-manpages.tar.bz2
Source3:	bind-dhcp-dynamic-dns-examples.tar.bz2
Source4:	bind-named.init
Source6:	bind-named.sysconfig
Source7:	bind-keygen.c
Source11:	ftp://ftp.internic.net/domain/named.cache
# (oe) http://mysql-bind.sourceforge.net/
Source12:	mysql-bind-0.1.tar.bz2
# caching-nameserver files (S100-S112)
Source100:	bogon_acl.conf
Source101:	hosts
Source102:	localdomain.zone
Source103:	localhost.zone
Source104:	logging.conf
Source105:	named.broadcast
Source106:	named.conf
Source107:	named.ip6.local
Source108:	named.local
Source109:	named.zero
Source110:	rndc.conf
Source111:	rndc.key
Source112:	trusted_networks_acl.conf
Source113:	named.iscdlv.key
Patch0:		bind-fallback-to-second-server.diff
Patch2:		bind-9.7.3-link.patch
Patch3:		bind-9.12.2-json-c.patch
Patch102:	bind-9.3.0rc2-sdb_mysql.patch
Patch205:	bind-9.3.2-prctl_set_dumpable.patch
Patch209:	bind-9.9-dlz-64bit.patch

BuildRequires:  file
%if %{sdb_mysql}
BuildRequires:	mysql-devel
%endif
%if %{with gssapi}
BuildRequires:	pkgconfig(krb5)
%endif
BuildRequires:	libcap-devel >= 2.10
BuildRequires:	geoip-devel
BuildRequires:	mysql-devel
BuildRequires:	openldap-devel
BuildRequires:	postgresql-devel
BuildRequires:	pkgconfig(libidn2)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(libcrypto)
BuildRequires:	pkgconfig(libssl)
BuildRequires:	pkgconfig(json-c)
BuildRequires:  readline-devel
BuildRequires:	lmdb-devel
BuildRequires:	rpm-helper

Requires:	bind-utils >= %{version}-%{release}
# takes care of MDV Bug #: 62829
Requires:	openssl-engines
Requires(pre,postun):	rpm-helper

%description
BIND (Berkeley Internet Name Domain) is an implementation of the DNS
(domain Name System) protocols. BIND includes a DNS server (named), 
which resolves host names to IP addresses, and a resolver library 
(routines for applications to use when interfacing with DNS).  A DNS 
server allows clients to name resources or objects and share the 
information with other network machines.  The named DNS server can be 
used on workstations as a caching name server, but is generally only 
needed on one machine for an entire network.  Note that the 
configuration files for making BIND act as a simple caching nameserver 
are included in the caching-nameserver package.  

Install the bind package if you need a DNS server for your network.  If
you want bind to act a caching name server, you will also need to install
the caching-nameserver package.

Many BIND 8 features previously unimplemented in BIND 9, including 
domain-specific forwarding, the \$GENERATE master file directive, and
the "blackhole", "dialup", and "sortlist" options Forwarding of dynamic
update requests; this is enabled by the "allow-update-forwarding" option 
A new, simplified database interface and a number of sample drivers based
on it; see doc/dev/sdb for details 
Support for building single-threaded servers for environments that do not 
supply POSIX threads 
New configuration options: "min-refresh-time", "max-refresh-time", 
"min-retry-time", "max-retry-time", "additional-from-auth",
"additional-from-cache", "notify explicit" 
Faster lookups, particularly in large zones. 

Build Options:
--with sdb_mysql      Build with MySQL database support
%package	utils
Summary:	Utilities for querying DNS name servers
Group:		Networking/Other

%description	utils
Bind-utils contains a collection of utilities for querying DNS (Domain
Name Service) name servers to find out information about Internet hosts.
These tools will provide you with the IP addresses for given host names,
as well as other information about registered domains and network 
addresses.

You should install bind-utils if you need to get information from DNS name
servers.

%package	devel
Summary:	Include files and libraries needed for bind DNS development
Group:		Development/C

%description	devel
The bind-devel package contains all the include files and the
library required for DNS (Domain Name Service) development for
BIND versions 9.x.x.

%package	doc
Summary:	Documentation for BIND
Group:		Books/Other

%description	doc
The bind-devel package contains the documentation for BIND.

%package -n python-isc
Summary:	Python bindings to the ISC library
Group:		Development/Python
BuildRequires:	pkgconfig(python3)
BuildRequires:	python-ply

%description -n python-isc
Python bindings to the ISC library.

%prep

%if "%plevel" != ""
%setup -q  -n %{name}-%{version}-%{plevel} -a2 -a3 -a12
%else
%setup -q  -n %{name}-%{version} -a2 -a3 -a12
%endif

%patch0 -p1 -b .fallback-to-second-server.droplet
%patch2 -p1 -b .link

%if %{sdb_mysql}
mv mysql-bind-0.1 contrib/sdb/mysql
%__cp contrib/sdb/mysql/mysqldb.c bin/named
%__cp contrib/sdb/mysql/mysqldb.h bin/named/include
%patch102 -p1 -b .sdb_mysql.droplet
%endif

%patch205 -p1 -b .prctl_set_dumpable.droplet
%patch209 -p1 -b .64bit

cp %{SOURCE4} named.init
# fix https://qa.mandriva.com/show_bug.cgi?id=62829
# so..., libgost.so needs to be in the chroot (ugly..., and will break backporting, well...)
OPENSSL_ENGINESDIR=$(grep '^#define ENGINESDIR' %{multiarch_includedir}/openssl/opensslconf.h | cut -d\" -f2 | sed -e 's/^\///')
perl -pi -e "s|_OPENSSL_ENGINESDIR_|$OPENSSL_ENGINESDIR|g" named.init

cp %{SOURCE6} named.sysconfig
cp %{SOURCE7} keygen.c
cp %{SOURCE11} named.cache

mkdir -p caching-nameserver
cp %{SOURCE100} caching-nameserver/bogon_acl.conf
cp %{SOURCE101} caching-nameserver/hosts
cp %{SOURCE102} caching-nameserver/localdomain.zone
cp %{SOURCE103} caching-nameserver/localhost.zone
cp %{SOURCE104} caching-nameserver/logging.conf
cp %{SOURCE105} caching-nameserver/named.broadcast
cp %{SOURCE106} caching-nameserver/named.conf
cp %{SOURCE107} caching-nameserver/named.ip6.local
cp %{SOURCE108} caching-nameserver/named.local
cp %{SOURCE109} caching-nameserver/named.zero
cp %{SOURCE110} caching-nameserver/rndc.conf
cp %{SOURCE111} caching-nameserver/rndc.key
cp %{SOURCE112} caching-nameserver/trusted_networks_acl.conf
cp %{SOURCE113} caching-nameserver/named.iscdlv.key

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'


%build
%serverbuild
# it does not work with -fPIE and someone added that to the serverbuild macro...
CFLAGS=$(echo $CFLAGS|sed -e 's|-fPIE||g')
CXXFLAGS=$(echo $CXXFLAGS|sed -e 's|-fPIE||g')

export CC=%{__cc}
export CXX=%{__cxx}
export CPPFLAGS="$CPPFLAGS -DDIG_SIGCHASE"
export STD_CDEFINES="$CPPFLAGS"

export WANT_AUTOCONF_2_5=1
libtoolize --copy --force; aclocal -I m4 --force; autoheader --force; autoconf --force

export CFLAGS="$CFLAGS -DLDAP_DEPRECATED"

# threading is evil for the host command
%configure \
	--localstatedir=/var \
	--disable-openssl-version-check \
	--disable-threads \
	--enable-largefile \
	--enable-ipv6 \
	--with-openssl=%{_prefix} \
	--with-libidn2 \
	--with-randomdev=/dev/urandom \
	--with-geoip
# FIXME configure should be fixed instead of having to work around
# its brokenness...
echo '#define HAVE_JSON_C 1' >>config.h

make -C lib
make -C bin/dig
make -C bin/dig DESTDIR="$(pwd)" install 
make clean

%configure \
	--localstatedir=/var \
	--disable-openssl-version-check \
	--enable-threads \
	--enable-largefile \
	--enable-ipv6 \
	--enable-filter-aaaa \
	--enable-epoll \
	--enable-native-pkcs11 \
	--with-openssl=%{_prefix} \
	--with-libidn2 \
%if %{with gssapi}
	--with-gssapi=%{_prefix} --disable-isc-spnego \
%else
	--without-gssapi \
%endif
	--with-randomdev=/dev/urandom \
	--with-libxml2=yes \
	--with-dlz-postgres=yes \
	--with-dlz-mysql=yes \
	--with-dlz-bdb=no \
	--with-dlz-filesystem=yes \
	--with-dlz-ldap=yes \
	--with-dlz-odbc=no \
	--with-dlz-stub=yes \
	--with-geoip
# FIXME configure should be fixed instead of having to work around
# its brokenness...
echo '#define HAVE_JSON_C 1' >>config.h

%make_build -j1

%if %{sdb_mysql}
cd contrib/sdb/mysql
%{__cc} $CFLAGS -I%{_includedir}/mysql -I../../../lib/dns/include -I../../../lib/dns/sec/dst/include \
  -I../../../lib/isc/include -I../../../lib/isc/unix/include -I../../../lib/isc/pthreads/include \
  -c zonetodb.c
%{_cc} $CFLAGS $LDFLAGS -o zonetodb zonetodb.o \
  ../../../lib/dns/libdns.a -lcrypto -lpthread ../../../lib/isc/libisc.a \
  -lmysqlclient -lresolv %{?_with_gssapi:$(krb5-config --libs gssapi)} -lxml2 -lGeoIP
cd -
%endif

%{__cc} $CFLAGS -o dns-keygen keygen.c

#%%check
## run the test suite
#make check

%install
cd doc
    rm -rf html
cd -

# make some directories
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}/var/run/named 

%make_install

ln -snf named %{buildroot}%{_sbindir}/lwresd

install -m0755 named.init %{buildroot}%{_initrddir}/named
install -m0644 named.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/named

%if %{sdb_mysql}
install -m0755 contrib/sdb/mysql/zonetodb %{buildroot}%{_bindir}/
cp contrib/sdb/mysql/ChangeLog contrib/sdb/mysql/ChangeLog.mysql
cp contrib/sdb/mysql/README contrib/sdb/mysql/README.mysql
%endif

install -m0755 dns-keygen %{buildroot}%{_sbindir}/dns-keygen

# install the non-threaded host command
# fixes #16855
install -m0755 usr/bin/host %{buildroot}%{_bindir}/

# make the chroot
install -d %{buildroot}/var/lib/named/{dev,etc}
install -d %{buildroot}/var/lib/named/var/{log,run,tmp}
install -d %{buildroot}/var/lib/named/var/named/{master,slaves,reverse,dynamic,data}

install -m 644 \
    caching-nameserver/named.conf \
    caching-nameserver/logging.conf \
    caching-nameserver/trusted_networks_acl.conf \
    caching-nameserver/hosts \
    caching-nameserver/bogon_acl.conf \
    %{buildroot}/var/lib/named/etc
install -m 640 \
    caching-nameserver/rndc.conf\
    caching-nameserver/rndc.key \
    caching-nameserver/named.iscdlv.key \
    %{buildroot}/var/lib/named/etc
install -m 644 \
    caching-nameserver/localdomain.zone \
    caching-nameserver/localhost.zone \
    %{buildroot}/var/lib/named/var/named/master
install -m 644 \
    caching-nameserver/named.broadcast  \
    caching-nameserver/named.ip6.local \
    caching-nameserver/named.local \
    caching-nameserver/named.zero \
    %{buildroot}/var/lib/named/var/named/reverse

# fix some compat symlinks
ln -s /var/lib/named/etc/named.conf %{buildroot}%{_sysconfdir}/named.conf
ln -s /var/lib/named/etc/rndc.conf %{buildroot}%{_sysconfdir}/rndc.conf
ln -s /var/lib/named/etc/rndc.key %{buildroot}%{_sysconfdir}/rndc.key
ln -s /var/lib/named/etc/named.iscdlv.key %{buildroot}%{_sysconfdir}/named.iscdlv.key
mv %{buildroot}%{_sysconfdir}/bind.keys %{buildroot}/var/lib/named/etc/
ln -s /var/lib/named/etc/bind.keys %{buildroot}%{_sysconfdir}/bind.keys

echo "; Use \"dig @A.ROOT-SERVERS.NET . ns\" to update this file if it's outdated." > named.cache.tmp
cat named.cache >> named.cache.tmp
install -m0644 named.cache.tmp %{buildroot}/var/lib/named/var/named/named.ca

# fix man pages
install -m0644 man5/resolver.5 %{buildroot}%{_mandir}/man5/
ln -s resolver.5 %{buildroot}%{_mandir}/man5/resolv.5

# the following 3 lines is needed to make it short-circuit compliant.
cd doc
    rm -rf html
cd -

install -d doc/html
cp -f $(find . -type f |grep html |sed -e 's#\/%{name}-%{version}##'|grep -v contrib) doc/html 

cat > README.urpmi << EOF
The most significant changes starting from the bind-9.3.2-5mdk package:

 o Installs in a chroot environment per default (/var/lib/named) for 
   security measures.

 o Acts as a caching only resolver per default, ip addresses that should be
   allowed to use recursive lookups must be defined in the 
   /var/lib/named/etc/trusted_networks_acl.conf file.
EOF

# this is just sick...
touch %{buildroot}/var/lib/named/var/named/dynamic/managed-keys.bind

%pre
%_pre_useradd named /var/lib/named /bin/false

# adjust home dir location if needed 
if [ "$(getent passwd named | awk -F: '{print $6}')" == "/var/named" ]; then
    usermod -d /var/lib/named named
fi

# check if bind is chrooted and try to restore it
if [ -x %{_sbindir}/bind-chroot.sh ]; then
    ROOTDIR="/var/lib/named-chroot"
    [ -f /etc/sysconfig/named ] && . /etc/sysconfig/named
    if [ -d $ROOTDIR -a ! -d /var/lib/named ]; then
	echo "old chroot found at $ROOTDIR, copying to /var/lib/named"
        cp -rp $ROOTDIR /var/lib/named
	chown -R named:named /var/lib/named
    fi
    if grep -q "$ROOTDIR" /etc/sysconfig/syslog; then
	if [ -f /var/lock/subsys/named ]; then
	    service named stop > /dev/null 2>/dev/null || :
	fi
	%{_sbindir}/bind-chroot.sh --unchroot > /dev/null 2>/dev/null || :
    fi
    if [ -f /var/lock/subsys/syslog ]; then
	service syslog restart  > /dev/null 2>/dev/null || :
    fi
fi

DATE=$(date +%%Y%%m%%d%%j%%S)
for f in named.conf rndc.conf rndc.key; do
    # move away files to prepare for softlinks
    if [ -f /etc/$f -a ! -h /etc/$f ]; then mv -vf /etc/$f /etc/$f.$DATE; fi
    if [ -f /etc/$f -a ! -h /etc/$f ]; then mv -vf /etc/$f /etc/$f.$DATE; fi
    if [ -f /etc/$f -a ! -h /etc/$f ]; then mv -vf /etc/$f /etc/$f.$DATE; fi
done

%post
if grep -q "_MY_KEY_" /var/lib/named/etc/rndc.conf /var/lib/named/etc/rndc.key; then
    MYKEY="$(%{_sbindir}/dns-keygen)"
    perl -pi -e "s|_MY_KEY_|$MYKEY|g" /var/lib/named/etc/rndc.conf /var/lib/named/etc/rndc.key
fi

%postun
%_postun_userdel named

%files -n python-isc
%{_prefix}/lib/python*/site-packages/isc*

%files
%doc README.urpmi
%config(noreplace) %{_sysconfdir}/sysconfig/named
%{_initrddir}/named
%{_sbindir}/ddns-confgen
%{_sbindir}/dns-keygen
%{_sbindir}/dnssec-checkds
%{_sbindir}/dnssec-coverage
%{_sbindir}/dnssec-dsfromkey
%{_sbindir}/dnssec-importkey
%{_sbindir}/dnssec-keyfromlabel
%{_sbindir}/dnssec-keygen
%{_sbindir}/dnssec-revoke
%{_sbindir}/dnssec-settime
%{_sbindir}/dnssec-signzone
%{_sbindir}/dnssec-verify
%{_sbindir}/lwresd
%{_sbindir}/named
%{_sbindir}/named-checkconf
%{_sbindir}/named-checkzone
%{_sbindir}/named-compilezone
%{_sbindir}/named-journalprint
%{_sbindir}/nsec3hash
%{_sbindir}/rndc
%{_sbindir}/rndc-confgen
%{_sbindir}/dnssec-cds
%{_sbindir}/dnssec-keymgr
%{_sbindir}/named-nzd2nzf
%{_sbindir}/pkcs11-*
%{_sbindir}/tsig-keygen
%{_libdir}/named/filter-aaaa.so
%{_mandir}/man1/arpaname.1.*
%{_mandir}/man5/named.conf.5*
%{_mandir}/man5/rndc.conf.5*
%{_mandir}/man8/ddns-confgen.8.*
%{_mandir}/man8/dnssec-*.8*
%{_mandir}/man8/filter-aaaa.8*
%{_mandir}/man8/named-*.8*
%{_mandir}/man8/named.8*
%{_mandir}/man8/nsec3hash.8.*
%{_mandir}/man8/pkcs11-*.8*
%{_mandir}/man8/rndc.8*
%{_mandir}/man8/rndc-confgen.8*
%{_mandir}/man8/tsig-keygen.8*
# the chroot
%dir /var/lib/named
%dir /var/lib/named/dev
%dir /var/lib/named/etc
%dir /var/lib/named/var
%dir /var/lib/named/var/named
%attr(-,named,named) %dir /var/lib/named/var/log
%attr(-,named,named) %dir /var/lib/named/var/run
%attr(-,named,named) %dir /var/lib/named/var/tmp
%attr(-,named,named) %dir /var/lib/named/var/named/master
%attr(-,named,named) %dir /var/lib/named/var/named/slaves
%attr(-,named,named) %dir /var/lib/named/var/named/reverse
%attr(-,named,named) %dir /var/lib/named/var/named/dynamic
%attr(-,named,named) %dir /var/lib/named/var/named/data
%config(noreplace) /var/lib/named/etc/named.conf
%attr(-,root,named) %config(noreplace) /var/lib/named/etc/bind.keys
%attr(-,root,named) %config(noreplace) /var/lib/named/etc/rndc.conf
%attr(-,root,named) %config(noreplace) /var/lib/named/etc/rndc.key
%attr(-,root,named) %config(noreplace) /var/lib/named/etc/named.iscdlv.key
%attr(-,named,named) /var/lib/named/var/named/dynamic/managed-keys.bind
%{_sysconfdir}/bind.keys
%{_sysconfdir}/named.conf
%{_sysconfdir}/rndc.conf
%{_sysconfdir}/rndc.key
%{_sysconfdir}/named.iscdlv.key
%config(noreplace) /var/lib/named/etc/bogon_acl.conf
%config(noreplace) /var/lib/named/etc/logging.conf
%config(noreplace) /var/lib/named/etc/trusted_networks_acl.conf
%config(noreplace) /var/lib/named/etc/hosts
%config(noreplace) /var/lib/named/var/named/master/localdomain.zone
%config(noreplace) /var/lib/named/var/named/master/localhost.zone
%config(noreplace) /var/lib/named/var/named/reverse/named.broadcast
%config(noreplace) /var/lib/named/var/named/reverse/named.ip6.local
%config(noreplace) /var/lib/named/var/named/reverse/named.local
%config(noreplace) /var/lib/named/var/named/reverse/named.zero
%config(noreplace) /var/lib/named/var/named/named.ca

%files devel
%{_bindir}/isc-config.sh
%{_bindir}/bind9-config
%{_includedir}/*
%{_libdir}/*.a
%{_mandir}/man1/bind9-config.1*
%{_mandir}/man1/isc-config.sh.1*

%files utils
%{_bindir}/dig
%{_bindir}/host
%{_bindir}/nslookup
%{_bindir}/nsupdate
%{_bindir}/arpaname
%{_bindir}/delv
%{_bindir}/mdig
%{_bindir}/named-rrchecker
%{_mandir}/man1/delv.1.xz
%{_mandir}/man1/mdig.1.xz
%{_mandir}/man1/named-rrchecker.1.xz
%{_mandir}/man1/host.1*
%{_mandir}/man1/dig.1*
%{_mandir}/man1/nslookup.1*
%{_mandir}/man1/nsupdate.1*
%{_mandir}/man5/resolver.5*
%{_mandir}/man5/resolv.5*

%files doc
%doc CHANGES README COPYRIGHT
%if %{sdb_mysql}
%doc contrib/sdb/mysql/ChangeLog.mysql contrib/sdb/mysql/README.mysql
%endif
%doc doc/html doc/misc/
%doc doc/dhcp-dynamic-dns-examples doc/chroot doc/trustix
