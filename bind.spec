%define Werror_cflags -Wformat
#define _disable_lto 1
# For plugins
%global _disable_ld_no_undefined 1

# default options
%bcond_without gssapi

Summary:	A DNS (Domain Name System) server
Name:		bind
Version:	9.21.19
Source0:	http://ftp.isc.org/isc/%{name}9/%{version}%{?plevel:-%plevel}/%{name}-%{version}%{?plevel:-%{plevel}}.tar.xz
Release:	1
License:	MPL-2.0
Group:		System/Servers
Url:		https://www.isc.org/bind/
Source1:	bind.sysusers
Source2:	bind-manpages.tar.bz2
Source3:	bind-dhcp-dynamic-dns-examples.tar.bz2
Source6:	bind-named.sysconfig
Source7:	bind-keygen.c
Source11:	ftp://ftp.internic.net/domain/named.cache
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

BuildRequires:	file
%if %{with gssapi}
BuildRequires:	pkgconfig(krb5)
BuildRequires:	pkgconfig(krb5-gssapi)
%endif
BuildRequires:	slibtool
BuildRequires:	pkgconfig(libcap)
BuildRequires:	pkgconfig(libmaxminddb)
BuildRequires:	pkgconfig(ldap)
BuildRequires:	postgresql-devel
BuildRequires:	pkgconfig(libidn2)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(libcrypto)
BuildRequires:	pkgconfig(libssl)
BuildRequires:	pkgconfig(json-c)
BuildRequires:	pkgconfig(libuv)
BuildRequires:	pkgconfig(readline)
BuildRequires:	pkgconfig(libnghttp2)
BuildRequires:	pkgconfig(liburcu)
BuildRequires:	pkgconfig(liburcu-cds)
BuildRequires:	pkgconfig(libfstrm)
BuildRequires:	pkgconfig(libprotobuf-c)
BuildRequires:	lmdb-devel
BuildRequires:	doxygen
BuildRequires:	xsltproc
BuildRequires:	python3dist(sphinx)
BuildRequires:	protobuf-compiler protobuf-c
%systemd_requires
Requires(pre):	systemd
Requires:	bind-utils >= %{version}-%{release}
# takes care of MDV Bug #: 62829
Requires:	openssl-engines

BuildSystem:	meson
BuildOption:	-Ddoc=enabled
BuildOption:	-Ddnstap=enabled
BuildOption:	-Ddoh=enabled
BuildOption:	-Dgeoip=enabled
%if %{with gssapi}
BuildOption:	-Dgssapi=enabled
%endif
BuildOption:	-Didn=enabled
BuildOption:	-Djemalloc=disabled
BuildOption:	-Dline=enabled
BuildOption:	-Dlmdb=enabled
BuildOption:	-Dstats-json=enabled
BuildOption:	-Dstats-xml=enabled
BuildOption:	-Dzlib=enabled

%patchlist
bind-fallback-to-second-server.diff
bind-9.3.2-prctl_set_dumpable.patch

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

%package utils
Summary:	Utilities for querying DNS name servers
Group:		Networking/Other

%description utils
Bind-utils contains a collection of utilities for querying DNS (Domain
Name Service) name servers to find out information about Internet hosts.
These tools will provide you with the IP addresses for given host names,
as well as other information about registered domains and network 
addresses.

You should install bind-utils if you need to get information from DNS name
servers.

# No point in separate libpackages because those are essentially internal use libraries
%package libs
Summary:	Libraries provided and used by bind
Group:		System/Libraries
# Not really, but something needs to compensate for the headers etc.
# having been removed upstream. Nothing used the libraries anyway...
Obsoletes:	%{name}-devel < %{EVRD}

%description libs
Libraries provided and used by bind

%package devel
Summary:	Include files and libraries needed for bind DNS development
Group:		Development/C
Requires:	%{name}-libs = %{EVRD}

%description devel
The bind-devel package contains all the include files and the
library required for DNS (Domain Name Service) development for
BIND versions 9.x.x.

%package doc
Summary:	Documentation for BIND
Group:		Books/Other

%description doc
The bind-devel package contains the documentation for BIND.

%prep -a
tar xf %{S:2}
tar xf %{S:3}

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

%build -a
%{__cc} $CFLAGS -o dns-keygen keygen.c

%install -a
# make some directories
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}/var/run/named 

ln -snf named %{buildroot}%{_bindir}/lwresd

install -m0644 named.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/named

install -m0755 dns-keygen %{buildroot}%{_bindir}/dns-keygen

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
cp bind.keys %{buildroot}/var/lib/named/etc/
ln -s /var/lib/named/etc/bind.keys %{buildroot}%{_sysconfdir}/bind.keys

echo "; Use \"dig @A.ROOT-SERVERS.NET . ns\" to update this file if it's outdated." > named.cache.tmp
cat named.cache >> named.cache.tmp
install -m0644 named.cache.tmp %{buildroot}/var/lib/named/var/named/named.ca

# fix man pages
install -D -m 0644 man5/resolver.5 %{buildroot}%{_mandir}/man5/resolver.5
ln -s resolver.5 %{buildroot}%{_mandir}/man5/resolv.5

# this is just sick...
touch %{buildroot}/var/lib/named/var/named/dynamic/managed-keys.bind
rm -rf %{buildroot}$RPM_BUILD_DIR

install -Dpm 644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}.conf

%post
if grep -q "_MY_KEY_" /var/lib/named/etc/rndc.conf /var/lib/named/etc/rndc.key; then
    MYKEY="$(%{_bindir}/dns-keygen)"
    sed -i -e "s|_MY_KEY_|$MYKEY|g" /var/lib/named/etc/rndc.conf /var/lib/named/etc/rndc.key
fi

%files
%config(noreplace) %{_sysconfdir}/sysconfig/named
%{_sysusersdir}/%{name}.conf
%{_bindir}/ddns-confgen
%{_bindir}/dns-keygen
%{_bindir}/lwresd
%{_bindir}/named
%{_bindir}/rndc
%{_bindir}/rndc-confgen
%{_bindir}/tsig-keygen
%{_bindir}/dnssec-cds
%{_bindir}/dnssec-dsfromkey
%{_bindir}/dnssec-importkey
%{_bindir}/dnssec-keyfromlabel
%{_bindir}/dnssec-keygen
%{_bindir}/dnssec-ksr
%{_bindir}/dnssec-revoke
%{_bindir}/dnssec-settime
%{_bindir}/dnssec-signzone
%{_bindir}/dnssec-verify
%{_bindir}/named-checkconf
%{_bindir}/named-checkzone
%{_bindir}/named-compilezone
%{_bindir}/named-journalprint
%{_bindir}/named-makejournal
%optional %{_bindir}/named-nzd2nzf
%{_bindir}/nsec3hash
%dir %{_libdir}/bind
%{_libdir}/bind/filter-a.so
%{_libdir}/bind/filter-aaaa.so
%{_libdir}/bind/synthrecord.so
%doc %{_mandir}/man1/arpaname.1*
%doc %{_mandir}/man1/dnssec-ksr.1*
%doc %{_mandir}/man5/named.conf.5*
%doc %{_mandir}/man5/rndc.conf.5*
%doc %{_mandir}/man8/rndc.8*
%doc %{_mandir}/man8/rndc-confgen.8*
%doc %{_mandir}/man8/tsig-keygen.8*
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
%doc %{_mandir}/man1/dnssec-cds.1*
%doc %{_mandir}/man1/dnssec-dsfromkey.1*
%doc %{_mandir}/man1/dnssec-importkey.1*
%doc %{_mandir}/man1/dnssec-keyfromlabel.1*
%doc %{_mandir}/man1/dnssec-keygen.1*
%doc %{_mandir}/man1/dnssec-revoke.1*
%doc %{_mandir}/man1/dnssec-settime.1*
%doc %{_mandir}/man1/dnssec-signzone.1*
%doc %{_mandir}/man1/dnssec-verify.1*
%doc %{_mandir}/man1/named-checkconf.1*
%doc %{_mandir}/man1/named-checkzone.1*
%doc %{_mandir}/man1/named-compilezone.1*
%doc %{_mandir}/man1/named-journalprint.1*
%doc %{_mandir}/man1/named-makejournal.1*
%optional %doc %{_mandir}/man1/named-nzd2nzf.1*
%doc %{_mandir}/man1/nsec3hash.1*
%doc %{_mandir}/man8/filter-aaaa.8*
%doc %{_mandir}/man8/named.8*
%doc %{_mandir}/man8/ddns-confgen.8*
%doc %{_mandir}/man8/filter-a.8*

%files libs
%{_libdir}/lib*.so

%files utils
%{_bindir}/dig
%{_bindir}/dnstap-read
%{_bindir}/host
%{_bindir}/nslookup
%{_bindir}/nsupdate
%{_bindir}/arpaname
%{_bindir}/delv
%{_bindir}/mdig
%{_bindir}/named-rrchecker
%doc %{_mandir}/man1/delv.1*
%doc %{_mandir}/man1/dnstap-read.1*
%doc %{_mandir}/man1/mdig.1*
%doc %{_mandir}/man1/named-rrchecker.1*
%doc %{_mandir}/man1/host.1*
%doc %{_mandir}/man1/dig.1*
%doc %{_mandir}/man1/nslookup.1*
%doc %{_mandir}/man1/nsupdate.1*
%doc %{_mandir}/man5/resolver.5*
%doc %{_mandir}/man5/resolv.5*

%files doc
%doc COPYRIGHT
%doc doc/misc/
%doc doc/dhcp-dynamic-dns-examples doc/chroot doc/trustix
