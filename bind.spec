# default options
%define sdb_ldap 1
%define sdb_mysql 0
%define geoip 0
%define gssapi 1

%{?_with_sdb_ldap: %{expand: %%global sdb_ldap 1}}
%{?_without_sdb_ldap: %{expand: %%global sdb_ldap 0}}
%{?_with_sdb_mysql: %{expand: %%global sdb_mysql 1}}
%{?_without_sdb_mysql: %{expand: %%global sdb_mysql 0}}
%{?_with_geoip: %{expand: %%global geoip 1}}
%{?_without_geoip: %{expand: %%global geoip 0}}
%{?_with_gssapi: %{expand: %%global gssapi 1}}
%{?_without_gssapi: %{expand: %%global gssapi 0}}

%if %{sdb_mysql}
%define sdb_ldap 0
%endif

%if %{sdb_ldap}
%define sdb_mysql 0
%endif

%if %{geoip}
%define geoip 1
%endif

%if %{gssapi}
%define gssapi 1
%endif

Summary:	A DNS (Domain Name System) server
Name:		bind
Version:	9.7.0
Release:	%mkrel 2
License:	Distributable
Group:		System/Servers
URL:		http://www.isc.org/products/BIND/
Source0:	ftp://ftp.isc.org/isc/%{name}9/%{version}/%{name}-%{version}.tar.gz
Source1:	ftp://ftp.isc.org/isc/%{name}9/%{version}/%{name}-%{version}.tar.gz.asc
Source2:	bind-manpages.tar.bz2
Source3:	bind-dhcp-dynamic-dns-examples.tar.bz2
Source4:	bind-named.init
Source6:	bind-named.sysconfig
Source7:	bind-keygen.c
Source11:	ftp://ftp.internic.net/domain/named.cache
# (oe) http://mysql-bind.sourceforge.net/
Source12:	mysql-bind-0.1.tar.bz2
# (oe) http://bind9-ldap.bayour.com/bind-sdb-ldap-1.0.tar.gz
Source13:	bind-sdb-ldap-1.0.tar.bz2
# (oe) http://www.blue-giraffe.com/zone2ldap/zone2ldap-0.4.tar.gz
Source14:	zone2ldap-0.4.tar.bz2
# (oe) http://www.venaas.no/dns/ldap2zone/
Source15:	ldap2zone.tar.bz2
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
Patch0:		bind-fallback-to-second-server.diff
Patch1:		bind-queryperf_fix.diff
Patch100:	bind-9.2.3-sdb_ldap.patch
Patch101:	bind-9.3.1-zone2ldap_fixes.diff
Patch102:	bind-9.3.0rc2-sdb_mysql.patch
Patch103:	zone2ldap-0.4-ldapv3.patch
Patch200:	bind-9.2.0rc3-varrun.patch
Patch204:	bind-9.4.0rc1-ppc-asm.patch
Patch205:	bind-9.3.2-prctl_set_dumpable.patch
Patch208:	bind-9.5-overflow.patch
Patch209:	bind-9.5-dlz-64bit.patch
Patch212:	bind-9.5-libidn.patch
Patch213:	bind-9.5-libidn2.patch
Patch215:	bind-9.5-libidn3.patch
Patch216:	bind95-rh461409.patch
Patch218:	bind-96-libtool2.patch
Patch219:	bind-95-rh452060.patch
Patch220:	bind93-rh490837.patch
Patch221:	bind-96-dyndb.patch
# (oe) rediffed patch originates from http://www.caraytech.com/geodns/
Patch300:	bind-9.4.0-geoip.diff
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires:	bind-utils >= %{version}-%{release}
BuildRequires:	openssl-devel
BuildRequires:	autoconf2.5
BuildRequires:	automake1.7
BuildRequires:  file
%if %{sdb_mysql}
BuildRequires:	mysql-devel
%endif
%if %{sdb_ldap}
BuildRequires:	openldap-devel
%endif
Obsoletes:	libdns0
Provides:	libdns0
%if %mdkversion >= 1020
BuildRequires:	multiarch-utils >= 1.0.3
%endif
Obsoletes:	caching-nameserver
Provides:	caching-nameserver
%if %{geoip}
BuildRequires:	libgeoip-devel
%endif
BuildRequires:	libidn-devel
BuildRequires:	postgresql-devel
BuildRequires:	mysql-devel
BuildRequires:	libcap-devel >= 2.10
%if %{gssapi}
BuildRequires:	krb5-devel
%endif
BuildRequires:	libxml2-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
--without sdb_ldap    Build without ldap simple database support (enabled
                      per default)
--with sdb_mysql      Build with MySQL database support (disables ldap
                      support, it's either way.)
--with geoip          Build with GeoIP support (disabled per default)

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

%prep

%setup -q  -n %{name}-%{version} -a2 -a3 -a12 -a13 -a14 -a15

%patch0 -p1 -b .fallback-to-second-server.droplet
%patch1 -p0 -b .queryperf_fix.droplet

%if %{sdb_ldap}
%__cp bind-sdb-ldap-*/ldapdb.c bin/named/
%__cp bind-sdb-ldap-*/ldapdb.h bin/named/include/
%patch100 -p1 -b .ldap_sdb.droplet
%patch101 -p0 -b .zone2ldap_fixes.droplet
%patch103 -p0 -b .ldapv3.droplet
%endif

%if %{sdb_mysql}
mv mysql-bind-0.1 contrib/sdb/mysql
%__cp contrib/sdb/mysql/mysqldb.c bin/named
%__cp contrib/sdb/mysql/mysqldb.h bin/named/include
%patch102 -p1 -b .sdb_mysql.droplet
%endif

%patch200 -p0 -b .varrun.droplet
%patch204 -p0 -b .no-register-names.droplet
%patch205 -p0 -b .prctl_set_dumpable.droplet
%patch208 -p1 -b .overflow.droplet
%patch209 -p0 -b .64bit

%patch212 -p1 -b .libidn
%patch213 -p1 -b .libidn2
%patch215 -p1 -b .libidn3
%patch216 -p1 -b .rh461409
mkdir -p m4
%patch218 -p1 -b .libtool2
%patch219 -p0 -b .rh452060
%patch220 -p0 -b .rh490837
%patch221 -p1 -b .dyndb

%if %{geoip}
%patch300 -p1 -b .geoip
%endif

cp %{SOURCE4} named.init
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

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build
%serverbuild

export CPPFLAGS="$CPPFLAGS -DDIG_SIGCHASE"
export STD_CDEFINES="$CPPFLAGS"

export WANT_AUTOCONF_2_5=1
libtoolize --copy --force; aclocal -I m4 --force; autoheader --force; autoconf --force

# (oe) make queryperf from the contrib _before_ bind..., makes it
# easier to determine if it builds or not, it saves time...
pushd contrib/queryperf
export WANT_AUTOCONF_2_5=1
rm -f configure
autoconf
%configure2_5x
%make CFLAGS="$CFLAGS"
popd

pushd contrib/query-loc-*
export WANT_AUTOCONF_2_5=1
perl -pi -e "s|-lnsl|-lnsl -lresolv|g" configure*
rm -f configure
autoconf
%configure2_5x
%make CFLAGS="$CFLAGS"
popd

export CFLAGS="$CFLAGS -DLDAP_DEPRECATED"

%if %{geoip}
export CFLAGS="$CFLAGS -DLDAP_DEPRECATED -DGEOIP"
export LDFLAGS="$LDFLAGS -lGeoIP"
%endif

# threading is evil for the host command
%configure \
    --localstatedir=/var \
    --disable-openssl-version-check \
    --disable-threads \
    --enable-largefile \
    --enable-ipv6 \
    --with-openssl=%{_prefix} \
    --with-randomdev=/dev/urandom

make -C lib
make -C bin/dig
make -C bin/dig DESTDIR="`pwd`" install 
make clean

%configure \
    --localstatedir=/var \
    --disable-openssl-version-check \
    --enable-threads \
    --enable-largefile \
    --enable-ipv6 \
    --enable-epoll \
    --with-openssl=%{_prefix} \
%if %{gssapi}
    --with-gssapi=%{_prefix} --disable-isc-spnego \
%endif
    --with-randomdev=/dev/urandom \
    --with-libxml2=yes \
    --with-dlz-postgres=yes \
    --with-dlz-mysql=yes \
    --with-dlz-bdb=no \
    --with-dlz-filesystem=yes \
    --with-dlz-ldap=yes \
    --with-dlz-odbc=no \
    --with-dlz-stub=yes

# pkcs11 support requires a working backend, otherwise bind won't start
# http://blogs.sun.com/janp/
# http://sourceforge.net/projects/opencryptoki
#--with-pkcs11 \

make

%if %{sdb_ldap}
pushd zone2ldap
# fix references to zone2ldap
perl -pi -e "s|zone2ldap|zonetoldap|g" *
    gcc $CFLAGS -I../lib/dns/include -I../lib/dns/sec/dst/include \
    -I../lib/isc/include -I../lib/isc/unix/include -I../lib/isc/pthreads/include -c zone2ldap.c
    gcc $CFLAGS -o zone2ldap zone2ldap.o ../lib/dns/libdns.a -lcrypto -lpthread \
    ../lib/isc/libisc.a -lldap -llber -lresolv %{?gssapi:-lgssapi_krb5} -lxml2 $LDFLAGS
popd

pushd ldap2zone
    gcc $CFLAGS -I../lib/dns/include -I../lib/dns/sec/dst/include \
    -I../lib/isc/include -I../lib/isc/unix/include -I../lib/isc/pthreads/include -c ldap2zone.c
    gcc $CFLAGS -o ldap2zone ldap2zone.o ../lib/dns/libdns.a -lcrypto -lpthread \
    ../lib/isc/libisc.a -lldap -llber -lresolv %{?_with_gssapi:-lgssapi_krb5} -lxml2 $LDFLAGS
popd
%endif

%if %{sdb_mysql}
pushd contrib/sdb/mysql
gcc $CFLAGS -I%{_includedir}/mysql -I../../../lib/dns/include -I../../../lib/dns/sec/dst/include \
  -I../../../lib/isc/include -I../../../lib/isc/unix/include -I../../../lib/isc/pthreads/include \
  -c zonetodb.c
gcc $CFLAGS -o zonetodb zonetodb.o \
  ../../../lib/dns/libdns.a -lcrypto -lpthread ../../../lib/isc/libisc.a \
  -lmysqlclient -lresolv %{?_with_gssapi:-lgssapi_krb5} -lxml2 $LDFLAGS
popd
%endif

gcc $CFLAGS -o dns-keygen keygen.c

#%%check
## run the test suite
#make check

%install
rm -rf %{buildroot}

pushd doc
    rm -rf html
popd

# make some directories
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}/var/run/named 

%makeinstall_std

ln -snf named %{buildroot}%{_sbindir}/lwresd

install -m0755 contrib/named-bootconf/named-bootconf.sh %{buildroot}%{_sbindir}/named-bootconf
install -m0755 contrib/queryperf/queryperf %{buildroot}%{_bindir}/
cp contrib/queryperf/README README.queryperf

install -m0755 contrib/query-loc-*/query-loc %{buildroot}%{_bindir}/
install -m0644 contrib/query-loc-*/query-loc.1 %{buildroot}%{_mandir}/man1/
cp contrib/query-loc-*/ADDRESSES ADDRESSES.query-loc
cp contrib/query-loc-*/ALGO ALGO.query-loc
cp contrib/query-loc-*/README README.query-loc
cp contrib/query-loc-*/USAGE USAGE.query-loc


install -m0755 named.init %{buildroot}%{_initrddir}/named
install -m0644 named.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/named

%if %{sdb_ldap}
install -m0755 zone2ldap/zone2ldap %{buildroot}%{_bindir}/zonetoldap
install -m0644 zone2ldap/zone2ldap.1 %{buildroot}%{_mandir}/man1/zonetoldap.1
install -m0755 ldap2zone/ldap2zone %{buildroot}%{_bindir}/ldap2zone
%endif

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
install -d %{buildroot}/var/lib/named/var/named/{master,slaves,reverse}

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
mv %{buildroot}%{_sysconfdir}/bind.keys %{buildroot}/var/lib/named/etc/
ln -s /var/lib/named/etc/bind.keys %{buildroot}%{_sysconfdir}/bind.keys

echo "; Use \"dig @A.ROOT-SERVERS.NET . ns\" to update this file if it's outdated." > named.cache.tmp
cat named.cache >> named.cache.tmp
install -m0644 named.cache.tmp %{buildroot}/var/lib/named/var/named/named.ca

# fix man pages
install -m0644 man5/resolver.5 %{buildroot}%{_mandir}/man5/
ln -s resolver.5 %{buildroot}%{_mandir}/man5/resolv.5

# the following 3 lines is needed to make it short-circuit compliant.
pushd doc
    rm -rf html
popd

install -d doc/html
cp -f `find . -type f |grep html |sed -e 's#\/%{name}-%{version}##'|grep -v contrib` doc/html 

%if %mdkversion >= 1020
%multiarch_binaries %{buildroot}%{_bindir}/isc-config.sh
%endif

cat > README.urpmi << EOF
The most significant changes starting from the bind-9.3.2-5mdk package:

 o Installs in a chroot environment per default (/var/lib/named) for 
   security measures.

 o Acts as a caching only resolver per default, ip addresses that should be
   allowed to use recursive lookups must be defined in the 
   /var/lib/named/etc/trusted_networks_acl.conf file.
EOF

%pre
%_pre_useradd named /var/lib/named /bin/false

# adjust home dir location if needed 
if [ "`getent passwd named | awk -F: '{print $6}'`" == "/var/named" ]; then
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

DATE=`date +%%Y%%m%%d%%j%%S`
for f in named.conf rndc.conf rndc.key; do
    # move away files to prepare for softlinks
    if [ -f /etc/$f -a ! -h /etc/$f ]; then mv -vf /etc/$f /etc/$f.$DATE; fi
    if [ -f /etc/$f -a ! -h /etc/$f ]; then mv -vf /etc/$f /etc/$f.$DATE; fi
    if [ -f /etc/$f -a ! -h /etc/$f ]; then mv -vf /etc/$f /etc/$f.$DATE; fi
done

%post
if grep -q "_MY_KEY_" /var/lib/named/etc/rndc.conf /var/lib/named/etc/rndc.key; then
    MYKEY="`%{_sbindir}/dns-keygen`"
    perl -pi -e "s|_MY_KEY_|$MYKEY|g" /var/lib/named/etc/rndc.conf /var/lib/named/etc/rndc.key
fi

%_post_service named

%preun
%_preun_service named

%postun
%_postun_userdel named

%triggerpostun -- bind < 8.2.2_P5-15
/sbin/chkconfig --add named

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGES README FAQ COPYRIGHT README.urpmi
%if %{sdb_ldap}
%doc contrib/sdb/ldap/README.ldap contrib/sdb/ldap/INSTALL.ldap
%endif
%if %{sdb_mysql}
%doc contrib/sdb/mysql/ChangeLog.mysql contrib/sdb/mysql/README.mysql
%endif
%if %{geoip}
%doc geodns.INSTALL geodns.named.conf-sample
%endif
%config(noreplace) %{_sysconfdir}/sysconfig/named
%{_initrddir}/named
%{_sbindir}/arpaname
%{_sbindir}/ddns-confgen
%{_sbindir}/dns-keygen
%{_sbindir}/dnssec-dsfromkey
%{_sbindir}/dnssec-keyfromlabel
%{_sbindir}/dnssec-keygen
%{_sbindir}/dnssec-revoke
%{_sbindir}/dnssec-settime
%{_sbindir}/dnssec-signzone
%{_sbindir}/genrandom
%{_sbindir}/isc-hmac-fixup
%{_sbindir}/lwresd
%{_sbindir}/named
%{_sbindir}/named-bootconf
%{_sbindir}/named-checkconf
%{_sbindir}/named-checkzone
%{_sbindir}/named-compilezone
%{_sbindir}/named-journalprint
%{_sbindir}/nsec3hash
%{_sbindir}/rndc
%{_sbindir}/rndc-confgen
%{_mandir}/man1/arpaname.1.*
%{_mandir}/man5/named.conf.5*
%{_mandir}/man5/rndc.conf.5*
%{_mandir}/man8/ddns-confgen.8.*
%{_mandir}/man8/dnssec-*.8*
%{_mandir}/man8/genrandom.8.*
%{_mandir}/man8/isc-hmac-fixup.8.*
%{_mandir}/man8/lwresd.8*
%{_mandir}/man8/named-*.8*
%{_mandir}/man8/named.8*
%{_mandir}/man8/nsec3hash.8.*
%{_mandir}/man8/rndc.8*
%{_mandir}/man8/rndc-confgen.8*
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
%config(noreplace) /var/lib/named/etc/named.conf
%attr(-,root,named) %config(noreplace) /var/lib/named/etc/bind.keys
%attr(-,root,named) %config(noreplace) /var/lib/named/etc/rndc.conf
%attr(-,root,named) %config(noreplace) /var/lib/named/etc/rndc.key
%{_sysconfdir}/bind.keys
%{_sysconfdir}/named.conf
%{_sysconfdir}/rndc.conf
%{_sysconfdir}/rndc.key
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
%defattr(-,root,root)
%doc CHANGES README
%if %mdkversion >= 1020
%multiarch %{multiarch_bindir}/isc-config.sh
%endif
%{_bindir}/isc-config.sh
%{_includedir}/*
%{_libdir}/*.a
%{_mandir}/man1/isc-config.sh.1*
%{_mandir}/man3/lwres*.3*

%files utils
%defattr(-,root,root)
%doc README COPYRIGHT *.query-loc *.queryperf
%{_bindir}/dig
%{_bindir}/host
%{_bindir}/nslookup
%{_bindir}/nsupdate
%{_bindir}/queryperf
%{_bindir}/query-loc
%{_mandir}/man1/host.1*
%{_mandir}/man1/dig.1*
%{_mandir}/man1/nslookup.1*
%{_mandir}/man1/nsupdate.1*
%{_mandir}/man1/query-loc.1*
%if %{sdb_ldap}
%doc zone2ldap/zone2ldap.README ldap2zone/README.ldap2zone ldap2zone/dnszone-schema.txt
%{_bindir}/zonetoldap
%{_bindir}/ldap2zone
%{_mandir}/man1/zonetoldap.1*
%endif
%{_mandir}/man5/resolver.5*
%{_mandir}/man5/resolv.5*

%files doc
%defattr(-,root,root)
%doc doc/draft doc/html doc/rfc doc/misc/
%doc doc/dhcp-dynamic-dns-examples doc/chroot doc/trustix
