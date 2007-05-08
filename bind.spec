# default options
%define sdb_ldap 1
%define sdb_mysql 0
%define geoip 0

%{?_with_sdb_ldap: %{expand: %%global sdb_ldap 1}}
%{?_without_sdb_ldap: %{expand: %%global sdb_ldap 0}}
%{?_with_sdb_mysql: %{expand: %%global sdb_mysql 1}}
%{?_without_sdb_mysql: %{expand: %%global sdb_mysql 0}}
%{?_with_geoip: %{expand: %%global geoip 1}}
%{?_without_geoip: %{expand: %%global geoip 0}}

%if %{sdb_mysql}
%define sdb_ldap 0
%endif

%if %{sdb_ldap}
%define sdb_mysql 0
%endif

%if %{geoip}
%define geoip 1
%endif
Summary:	A DNS (Domain Name System) server
Name:		bind
Version:	9.4.1
Release:	%mkrel 1
License:	distributable
Group:		System/Servers
URL:		http://www.isc.org/products/BIND/
Source0:	ftp://ftp.isc.org/isc/%{name}9/%{version}/%{name}-%{version}.tar.gz
Source1:	ftp://ftp.isc.org/isc/%{name}9/%{version}/%{name}-%{version}.tar.gz.asc
Source2:	bind-manpages.tar.bz2
Source3:	bind-dhcp-dynamic-dns-examples.tar.bz2
Source4:	bind-named.init
Source5:	bind-named.logrotate
Source6:	bind-named.sysconfig
Source7:	bind-keygen.c
Source10:	caching-nameserver.tar.bz2
Source11:	bind-named.root
# (oe) http://mysql-bind.sourceforge.net/
Source12:	mysql-bind-0.1.tar.bz2
# (oe) http://www.venaas.no/ldap/bind-sdb/bind-sdb-ldap-1.0.tar.gz
Source13:	bind-sdb-ldap-1.0.tar.bz2
# (oe) http://www.blue-giraffe.com/zone2ldap/zone2ldap-0.4.tar.gz
Source14:	zone2ldap/zone2ldap-0.4.tar.bz2
# (oe) http://www.venaas.no/dns/ldap2zone/
Source15:	ldap2zone.tar.bz2
# (oe) these tools were removed, no reason given...
Source16:	bind-9.3.1-missing_tools.tar.gz
Patch0:		bind-fallback-to-second-server.diff
Patch1:		bind-9.3.0-libresolv.patch
Patch3:		bind-9.3.0beta2-libtool.diff
Patch100:	bind-9.2.3-sdb_ldap.patch
Patch101:	bind-9.3.1-zone2ldap_fixes.diff
Patch102:	bind-9.3.0rc2-sdb_mysql.patch
Patch103:	zone2ldap-0.4-ldapv3.patch
Patch200:	bind-9.2.0rc3-varrun.patch
Patch201:	bind-9.3.0-handle-send-errors.patch
Patch202:	bind-9.3.2b1-missing-dnssec-tools.diff
Patch203:	libbind-9.3.1rc1-fix_h_errno.patch
Patch204:	bind-9.4.0rc1-ppc-asm.patch
Patch205:	bind-9.3.2-prctl_set_dumpable.patch
Patch206:	bind-9.3.3-edns.patch
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
BuildRequires:	MySQL-devel
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
BuildRoot:	%{_tmppath}/%{name}-buildroot

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

%prep

%setup -q  -n %{name}-%{version} -a2 -a3 -a10 -a12 -a13 -a14 -a15 -a16
%patch0 -p1 -b .fallback-to-second-server.droplet
%patch1 -p1 -b .libresolv.droplet
%patch3 -p1 -b .libtool.droplet

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

%patch200 -p1 -b .varrun.droplet
#%patch201 -p1 -b .handle_send_errors
%patch202 -p0 -b .missing_dnssec_tools.droplet
%patch203 -p1 -b .fix_h_errno.droplet
%patch204 -p1 -b .no-register-names
%patch205 -p1 -b .prctl_set_dumpable
%patch206 -p1 -b .edns

%if %{geoip}
%patch300 -p1 -b .geoip
%endif

cp %{SOURCE4} named.init
cp %{SOURCE5} named.logrotate
cp %{SOURCE6} named.sysconfig
cp %{SOURCE7} keygen.c
cp %{SOURCE11} named.cache

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build

# (oe) make queryperf from the contrib _before_ bind..., makes it
# easier to determine if it builds or not, it saves time...
pushd contrib/queryperf
export WANT_AUTOCONF_2_5=1
rm -f configure
autoconf
%configure2_5x
%make CFLAGS="%{optflags}"
popd

export CFLAGS="-O2 -Wall -pipe -DLDAP_DEPRECATED"

%if %{geoip}
export CFLAGS="-O2 -Wall -pipe -DLDAP_DEPRECATED -DGEOIP"
export LDFLAGS="$LDFLAGS -lGeoIP"
%endif

# threading is evil for the host command
%configure \
    --localstatedir=/var \
    --disable-openssl-version-check \
    --disable-threads \
    --enable-largefile \
    --enable-ipv6 \
    --with-openssl=%{_includedir}/openssl \
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
    --with-openssl=%{_includedir}/openssl \
    --with-randomdev=/dev/urandom

make

# run the test suite
#make check

%if %{sdb_ldap}
pushd zone2ldap
# fix references to zone2ldap
perl -pi -e "s|zone2ldap|zonetoldap|g" *
    gcc $CFLAGS -I../lib/dns/include -I../lib/dns/sec/dst/include \
    -I../lib/isc/include -I../lib/isc/unix/include -I../lib/isc/pthreads/include -c zone2ldap.c
    gcc $CFLAGS -o zone2ldap zone2ldap.o ../lib/dns/libdns.a  -lcrypto -lpthread \
    ../lib/isc/libisc.a -lldap -llber -lresolv $LDFLAGS
popd

pushd ldap2zone
    gcc $CFLAGS -I../lib/dns/include -I../lib/dns/sec/dst/include \
    -I../lib/isc/include -I../lib/isc/unix/include -I../lib/isc/pthreads/include -c ldap2zone.c
    gcc $CFLAGS -o ldap2zone ldap2zone.o ../lib/dns/libdns.a  -lcrypto -lpthread \
    ../lib/isc/libisc.a -lldap -llber -lresolv $LDFLAGS
popd
%endif

%if %{sdb_mysql}
pushd contrib/sdb/mysql
gcc $CFLAGS -I%{_includedir}/mysql -I../../../lib/dns/include -I../../../lib/dns/sec/dst/include \
  -I../../../lib/isc/include -I../../../lib/isc/unix/include -I../../../lib/isc/pthreads/include \
  -c zonetodb.c
gcc $CFLAGS -o zonetodb zonetodb.o \
  ../../../lib/dns/libdns.a  -lcrypto -lpthread ../../../lib/isc/libisc.a \
  -lmysqlclient -lresolv $LDFLAGS
popd
%endif

gcc %{optflags} -o dns-keygen keygen.c

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

pushd doc
    rm -rf html
popd

# make some directories
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sysconfdir}/{logrotate.d,sysconfig}
install -d %{buildroot}/var/run/named 
install -d %{buildroot}/var/log/named 

%makeinstall_std

ln -snf named %{buildroot}%{_sbindir}/lwresd

install -m0755 contrib/named-bootconf/named-bootconf.sh %{buildroot}%{_sbindir}/named-bootconf
install -m0755 contrib/queryperf/queryperf %{buildroot}%{_sbindir}/
cp contrib/queryperf/README contrib/queryperf/README.queryperf

install -m0755 named.init %{buildroot}%{_initrddir}/named
install -m0644 named.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/named
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
install -d %{buildroot}%{_localstatedir}/named/{dev,etc}
install -d %{buildroot}%{_localstatedir}/named/var/{log,run,tmp}
install -d %{buildroot}%{_localstatedir}/named/var/named/{master,slaves,reverse}

install -m 644 \
    caching-nameserver/named.conf \
    caching-nameserver/logging.conf \
    caching-nameserver/trusted_networks_acl.conf \
    caching-nameserver/hosts \
    caching-nameserver/bogon_acl.conf \
    %{buildroot}%{_localstatedir}/named/etc
install -m 640 \
    caching-nameserver/rndc.conf\
    caching-nameserver/rndc.key \
    %{buildroot}%{_localstatedir}/named/etc
install -m 644 \
    caching-nameserver/localdomain.zone \
    caching-nameserver/localhost.zone \
    %{buildroot}%{_localstatedir}/named/var/named/master
install -m 644 \
    caching-nameserver/named.broadcast  \
    caching-nameserver/named.ip6.local \
    caching-nameserver/named.local \
    caching-nameserver/named.zero \
    %{buildroot}%{_localstatedir}/named/var/named/reverse

# fix some compat symlinks
ln -s %{_localstatedir}/named/etc/named.conf %{buildroot}%{_sysconfdir}/named.conf
ln -s %{_localstatedir}/named/etc/rndc.conf %{buildroot}%{_sysconfdir}/rndc.conf
ln -s %{_localstatedir}/named/etc/rndc.key %{buildroot}%{_sysconfdir}/rndc.key

echo "; Use \"dig @A.ROOT-SERVERS.NET . ns\" to update this file if it's outdated." > named.cache.tmp
cat named.cache >> named.cache.tmp
install -m0644 named.cache.tmp %{buildroot}%{_localstatedir}/named/var/named/named.ca

# fix man pages
install -m0644 man5/resolver.5 %{buildroot}%{_mandir}/man5/
ln -s resolver.5.bz2 %{buildroot}%{_mandir}/man5/resolv.5.bz2

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
%_pre_useradd named %{_localstatedir}/named /bin/false

# adjust home dir location if needed 
if [ "`getent passwd named | awk -F: '{print $6}'`" == "/var/named" ]; then
    usermod -d %{_localstatedir}/named named
fi

# check if bind is chrooted and try to restore it
if [ -x %{_sbindir}/bind-chroot.sh ]; then
    ROOTDIR="%{_localstatedir}/named-chroot"
    [ -f /etc/sysconfig/named ] && . /etc/sysconfig/named
    if [ -d $ROOTDIR -a ! -d %{_localstatedir}/named ]; then
	echo "old chroot found at $ROOTDIR, copying to %{_localstatedir}/named"
        cp -rp $ROOTDIR %{_localstatedir}/named
	chown -R named:named %{_localstatedir}/named
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
if grep -q "_MY_KEY_" %{_localstatedir}/named/etc/rndc.conf %{_localstatedir}/named/etc/rndc.key; then
    MYKEY="`%{_sbindir}/dns-keygen`"
    perl -pi -e "s|_MY_KEY_|$MYKEY|g" %{_localstatedir}/named/etc/rndc.conf %{_localstatedir}/named/etc/rndc.key
fi

%_post_service named

%preun
%_preun_service named

%postun
%_postun_userdel named

%triggerpostun -- bind < 8.2.2_P5-15
/sbin/chkconfig --add named

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGES README FAQ COPYRIGHT README.urpmi
%doc contrib/queryperf/README.queryperf
%doc doc/draft doc/html doc/rfc doc/misc/
%doc doc/dhcp-dynamic-dns-examples doc/chroot doc/trustix
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
%config(noreplace) %{_sysconfdir}/logrotate.d/named
%{_initrddir}/named
%{_sbindir}/dns-keygen
%{_sbindir}/dnssec-keygen
%{_sbindir}/dnssec-makekeyset
%{_sbindir}/dnssec-signkey
%{_sbindir}/dnssec-signzone
%{_sbindir}/lwresd
%{_sbindir}/named
%{_sbindir}/named-bootconf
%{_sbindir}/named-checkconf
%{_sbindir}/named-checkzone
%{_sbindir}/named-compilezone
%{_sbindir}/queryperf
%{_sbindir}/rndc
%{_sbindir}/rndc-confgen
%{_mandir}/man3/lwres*.3*
%{_mandir}/man5/rndc.conf.5*
%{_mandir}/man5/named.conf.5*
%{_mandir}/man8/rndc.8*
%{_mandir}/man8/rndc-confgen.8*
%{_mandir}/man8/named.8*
%{_mandir}/man8/dnssec-*.8*
%{_mandir}/man8/lwresd.8*
%{_mandir}/man8/named-*.8*
# the chroot
%dir %{_localstatedir}/named
%dir %{_localstatedir}/named/dev
%dir %{_localstatedir}/named/etc
%dir %{_localstatedir}/named/var
%dir %{_localstatedir}/named/var/named
%attr(-,named,named) %dir %{_localstatedir}/named/var/log
%attr(-,named,named) %dir %{_localstatedir}/named/var/run
%attr(-,named,named) %dir %{_localstatedir}/named/var/tmp
%attr(-,named,named) %dir %{_localstatedir}/named/var/named/master
%attr(-,named,named) %dir %{_localstatedir}/named/var/named/slaves
%attr(-,named,named) %dir %{_localstatedir}/named/var/named/reverse
%config(noreplace) %{_localstatedir}/named/etc/named.conf
%attr(-,root,named) %config(noreplace) %{_localstatedir}/named/etc/rndc.conf
%attr(-,root,named) %config(noreplace) %{_localstatedir}/named/etc/rndc.key
%{_sysconfdir}/named.conf
%{_sysconfdir}/rndc.conf
%{_sysconfdir}/rndc.key
%config(noreplace) %{_localstatedir}/named/etc/bogon_acl.conf
%config(noreplace) %{_localstatedir}/named/etc/logging.conf
%config(noreplace) %{_localstatedir}/named/etc/trusted_networks_acl.conf
%config(noreplace) %{_localstatedir}/named/etc/hosts
%config(noreplace) %{_localstatedir}/named/var/named/master/localdomain.zone
%config(noreplace) %{_localstatedir}/named/var/named/master/localhost.zone
%config(noreplace) %{_localstatedir}/named/var/named/reverse/named.broadcast
%config(noreplace) %{_localstatedir}/named/var/named/reverse/named.ip6.local
%config(noreplace) %{_localstatedir}/named/var/named/reverse/named.local
%config(noreplace) %{_localstatedir}/named/var/named/reverse/named.zero
%config(noreplace) %{_localstatedir}/named/var/named/named.ca

%files devel
%defattr(-,root,root)
%doc CHANGES README
%if %mdkversion >= 1020
%multiarch %{multiarch_bindir}/isc-config.sh
%endif
%{_bindir}/isc-config.sh
%{_includedir}/*
%{_libdir}/*.a

%files utils
%defattr(-,root,root)
%doc README COPYRIGHT
%{_bindir}/dig
%{_bindir}/host
%{_bindir}/nslookup
%{_bindir}/nsupdate
%{_mandir}/man1/host.1*
%{_mandir}/man1/dig.1*
%{_mandir}/man1/nslookup.1*
%if %{sdb_ldap}
%doc zone2ldap/zone2ldap.README ldap2zone/README.ldap2zone ldap2zone/dnszone-schema.txt
%{_bindir}/zonetoldap
%{_bindir}/ldap2zone
%{_mandir}/man1/zonetoldap.1*
%endif
%{_mandir}/man8/nsupdate.8*
%{_mandir}/man5/resolver.5*
%{_mandir}/man5/resolv.5*
