%bcond_with testsuite
%bcond_without clustering

%define talloc_version 2.1.14
%define tdb_version 1.3.16
%define tevent_version 0.9.37
%define ldb_version 1.4.2

%undefine _strict_symbol_defs_build

%global with_libsmbclient 1
%global with_libwbclient 1
%global with_profiling 1
%global with_vfs_cephfs 0

%global with_vfs_glusterfs 0
%ifarch x86_64
%global with_vfs_glusterfs 1
%endif

%global with_intel_aes_accel 0
%ifarch x86_64
%global with_intel_aes_accel 1
%endif

%global libwbc_alternatives_version 0.14
%global libwbc_alternatives_suffix %nil
%if 0%{?__isa_bits} == 64
%global libwbc_alternatives_suffix -64
%endif

%global with_mitkrb5 1

%global with_dc 1
%if %{with testsuite}
%global with_dc 1
%endif

%global required_mit_krb5 1.15.1

%global with_clustering_support 0
%if %{with clustering}
%global with_clustering_support 1
%endif

%{!?python2_sitearch: %define python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%global _systemd_extra "Environment=KRB5CCNAME=FILE:/run/samba/krb5cc_samba"
%define samba_depver %{version}-%{release}

Name:           samba
Version:        4.9.1
Release:        9
Summary:        A suite for Linux to interoperate with Windows
License:        GPLv3+ and LGPLv3+
URL:            http://www.samba.org/
Source0:        https://download.samba.org/pub/samba/stable/%{name}-%{version}.tar.gz
Source1:        https://download.samba.org/pub/samba/stable/%{name}-%{version}.tar.asc
Source2:        gpgkey-52FBC0B86D954B0843324CDC6F33915B6568B7EA.gpg
Source3:        samba.log
Source4:        smb.conf.vendor
Source5:        smb.conf.example
Source6:        pam_winbind.conf
Source7:        samba.pamd

Patch6000:      samba-4.9.0rc5-stack-protector.patch
Patch6001:      CVE-2018-14629.patch
Patch6002:      CVE-2018-16851.patch
Patch6003:      CVE-2018-16853-1.patch
Patch6004:      CVE-2018-16853-2.patch
Patch6005:      CVE-2019-3870-1.patch
Patch6006:      CVE-2019-3870-2.patch
Patch6007:      CVE-2019-3870-3.patch
Patch6008:      CVE-2019-3870-4.patch
Patch6009:      CVE-2019-3870-5.patch
Patch6010:      CVE-2019-3880.patch
Patch6011:      CVE-2018-16841-1.patch
Patch6012:      CVE-2018-16841-2.patch
Patch6013:      CVE-2019-12435-1.patch
Patch6014:      CVE-2019-12435-2.patch
Patch6015:      CVE-2018-16852-1.patch
Patch6016:      CVE-2018-16852-2.patch
Patch6017:      CVE-2018-16852-3.patch
Patch6018:      CVE-2018-16857-1.patch
Patch6019:      CVE-2018-16857-2.patch
Patch6020:      CVE-2018-16857-3.patch
Patch6021:      CVE-2018-16857-4.patch
Patch6022:      CVE-2018-16857-5.patch
Patch6023:      CVE-2018-16857-6.patch
Patch6024:      CVE-2018-16857-7.patch
Patch6025:      CVE-2018-16857-8.patch
Patch6026:      CVE-2018-16857-9.patch
Patch6027:      CVE-2019-10197-1.patch
Patch6028:      CVE-2019-10197-2.patch
Patch6029:      CVE-2019-10197-3.patch
Patch6030:      CVE-2019-10197-4.patch
Patch6031:      CVE-2019-10197-5.patch
Patch6032:      CVE-2019-10197-6.patch
Patch6033:      0001-CVE-2019-14847.patch
Patch6034:      0002-CVE-2019-14847.patch
Patch6035:      0003-CVE-2019-14847.patch
Patch6036:      0001-CVE-2019-14833.patch
Patch6037:      0002-CVE-2019-14833.patch
Patch6038:      0001-CVE-2019-10218.patch
Patch6039:      0002-CVE-2019-10218.patch
Patch6040:      0001-CVE-2019-3824.patch
Patch6041:      0002-CVE-2019-3824.patch
Patch6042:      0003-CVE-2019-3824.patch
Patch6043:      0004-CVE-2019-3824.patch
Patch6044:      0005-CVE-2019-3824.patch
Patch6045:      0006-CVE-2019-3824.patch
Patch6046:      0007-CVE-2019-3824.patch
Patch6047:      CVE-2019-14861.patch
Patch6048:      CVE-2019-14870.patch
Patch6049:      CVE-2018-16860.patch

BuildRequires:  avahi-devel cups-devel dbus-devel docbook-style-xsl e2fsprogs-devel gawk gnupg2 gpgme-devel
BuildRequires:  jansson-devel krb5-devel >= %{required_mit_krb5} libacl-devel libaio-devel libarchive-devel
BuildRequires:  libattr-devel libcap-devel libcmocka-devel libnsl2-devel libtirpc-devel libuuid-devel
BuildRequires:  libxslt ncurses-devel openldap-devel pam-devel perl-generators perl(Test::More)
BuildRequires:  perl(ExtUtils::MakeMaker) perl(Parse::Yapp) popt-devel python2-devel python3-devel
%if %{with_dc}
BuildRequires:  python2-dns python2-iso8601 python3-iso8601
%endif
BuildRequires:  quota-devel readline-devel rpcgen rpcsvc-proto-devel sed xfsprogs-devel xz zlib-devel >= 1.2.3
BuildRequires:  pkgconfig(libsystemd)
%if %{with_vfs_glusterfs}
BuildRequires:  glusterfs-api-devel >= 3.4.0.16 glusterfs-devel >= 3.4.0.16
%endif
%if %{with_vfs_cephfs}
BuildRequires:  libcephfs-devel
%endif
%if %{with_dc}
BuildRequires:  bind gnutls-devel >= 3.4.7 krb5-server >= %{required_mit_krb5} python2-crypto python3-crypto
%endif
BuildRequires:  perl(Parse::Yapp) libtalloc-devel >= %{talloc_version} python2-talloc-devel >= %{talloc_version}
BuildRequires:  python3-talloc-devel >= %{talloc_version} libtevent-devel >= %{tevent_version}
BuildRequires:  python2-tevent >= %{tevent_version} python3-tevent >= %{tevent_version}
BuildRequires:  libtdb-devel >= %{tdb_version} python2-tdb >= %{tdb_version} python3-tdb >= %{tdb_version}
BuildRequires:  libldb-devel >= %{ldb_version} python2-ldb-devel >= %{ldb_version}
BuildRequires:  python3-ldb-devel >= %{ldb_version}
%if %{with testsuite}
BuildRequires:  ldb-tools tdb-tools python2-pygpgme python2-markdown python3-pygpgme python3-markdown
%endif
%if %{with_dc}
BuildRequires:  krb5-server >= %{required_mit_krb5} bind
%endif

Requires:       systemd shadow-utils pam %{name}-common = %{samba_depver}
Requires:       %{name}-common = %{samba_depver} %{name}-common-tools = %{samba_depver}
Requires:       %{name}-client = %{samba_depver}
%if %with_libwbclient
Requires:       libwbclient = %{samba_depver}
%endif

Provides:       samba4 = %{samba_depver} samba-doc = %{samba_depver} samba-domainjoin-gui = %{samba_depver}
Provides:       samba-swat = %{samba_depver} samba4-swat = %{samba_depver} %{name}-libs = %{samba_depver}
Provides:       samba4-libs = %{samba_depver}
Obsoletes:      samba4 < %{samba_depver} samba-doc < %{samba_depver} samba-domainjoin-gui < %{samba_depver}
Obsoletes:      samba-swat < %{samba_depver} samba4-swat < %{samba_depver} %{name}-libs < %{samba_depver}
Obsoletes:      samba4-libs < %{samba_depver}

%description
Samba is a suite of programs for Linux and Unix to interoperate with Windows.

%package client
Summary:        Client package for %{name}
Requires:       %{name}-common = %{samba_depver}
Requires:       chkconfig krb5-libs >= %{required_mit_krb5}
%if %with_libwbclient
Requires:       libwbclient = %{samba_depver}
%endif
%if %with_libsmbclient
Requires:       libsmbclient = %{samba_depver}
%endif
Provides:       samba4-client = %{samba_depver} %{name}-client-libs
Obsoletes:      samba4-client < %{samba_depver} %{name}-client-libs

%description client
This package includes some files about SMB/CIFS clients to complement
the SMB/CIFS filesystem.

%package common
Summary:        Common package for %{name} client and server
Requires:       systemd
Requires:       %{name}-client = %{samba_depver}
%if %with_libwbclient
Requires:       libwbclient = %{samba_depver}
%endif
Provides:       samba4-common = %{samba_depver} %{name}-common-libs
Obsoletes:      samba4-common < %{samba_depver} %{name}-common-libs

%description common
This package contains some common basic files needed by %{name} client
and server.

%package common-tools
Summary:        Tools package for %{name}
Requires:       %{name}-common = %{samba_depver} %{name}-client = %{samba_depver} %{name} = %{samba_depver}
%if %with_libwbclient
Requires:       libwbclient = %{samba_depver}
%endif

%description common-tools
This package contains some tools for %{name} server and client.

%package dc
Summary:        Domain Controller package for %{name}
Requires:       %{name} = %{samba_depver} %{name}-winbind = %{samba_depver}
Requires:       %{name}-common = %{samba_depver} tdb-tools
%if %{with_dc}
Requires:       python2 python2-%{name} = %{samba_depver} python2-%{name}-dc = %{samba_depver}
Requires:       python2-crypto krb5-server >= %{required_mit_krb5}
# needs libldb and samba version are the same. Otherwise samba-tools
# will not work
%requires_eq libldb
%endif
Provides:       samba4-dc = %{samba_depver} %{name}-dc-libs samba4-dc-libs = %{samba_depver}
Obsoletes:      samba4-dc < %{samba_depver} %{name}-dc-libs samba4-dc-libs < %{samba_depver}

%description dc
The samba-dc package provides AD Domain Controller functionality, including some
libraries.

%if %{with_dc}
%package dc-bind-dlz
Summary:        Bind DLZ module for Samba AD
Requires:       %{name}-common = %{samba_depver} %{name}-dc = %{samba_depver} bind

%description dc-bind-dlz
This package contains the library files to manage name server related details of
Samba AD.
%endif

%package devel
Summary:        Development package for %{name}
Requires:       %{name} = %{samba_depver} %{name}-client = %{samba_depver}
Provides:       samba4-devel = %{samba_depver}
Obsoletes:      samba4-devel < %{samba_depver}

%description devel
This package contains some header files and library files for %{name}.

%if %{with_vfs_cephfs}
%package vfs-cephfs
Summary:        The VFS module for Ceph distributed storage system
Requires:       %{name} = %{samba_depver}

%description vfs-cephfs
This is the samba VFS module for Ceph distributed storage system integration.
%endif

%if %{with_vfs_glusterfs}
%package vfs-glusterfs
Summary:        The VFS module for GlusterFS
Requires:       glusterfs-api >= 3.4.0.16 glusterfs >= 3.4.0.16
Requires:       %{name} = %{samba_depver} %{name}-client = %{samba_depver}
Obsoletes:      samba-glusterfs < %{samba_depver}
Provides:       samba-glusterfs = %{samba_depver}

%description vfs-glusterfs
This is the samba VFS module for GlusterFS integration.
%endif

%package krb5-printing
Summary:        The samba CUPS backend package for printing with Kerberos
Requires:       %{name}-client chkconfig

%description krb5-printing
This package will allow cups to access the Kerberos credentials cache
of the user issuing the print job.

%if %with_libsmbclient
%package -n libsmbclient
Summary:        The SMB client library package for %{name}
Requires:       %{name}-common = %{samba_depver} %{name}-client = %{samba_depver}

%description -n libsmbclient
This pacakge contains the SMB client library from the Samba suite.

%package -n libsmbclient-devel
Summary:        Development package for the SMB client library
Requires:       libsmbclient = %{samba_depver}

%description -n libsmbclient-devel
This package contains some head files and libraries for libsmbclient package.
%endif

%if %with_libwbclient
%package -n libwbclient
Summary:        The winbind client library for %{name}
Requires:       %{name}-client = %{samba_depver}

%description -n libwbclient
This package contains the winbind client library from the Samba.

%package -n libwbclient-devel
Summary:        The development package for the winbind library
Requires:       libwbclient = %{samba_depver}
Provides:       samba-winbind-devel = %{samba_depver}
Obsoletes:      samba-winbind-devel < %{samba_depver}

%description -n libwbclient-devel
This package provides developer tools for the wbclient library.
%endif

%if %{with_dc}
%package -n python2-%{name}
Summary:        Python libraries for %{name}
Requires:       %{name} = %{samba_depver} %{name}-client = %{samba_depver} %{name}-common = %{samba_depver}
Requires:       python2-tevent python2-tdb python2-ldb python2-talloc python2-dns
Provides:       samba-python = %{samba_depver} samba4-python = %{samba_depver}
Obsoletes:      samba-python < %{samba_depver} samba4-python < %{samba_depver}

%description -n python2-%{name}
This package contains the Python libraries needed by programs to use SMB, RPC
 and other Samba provided protocols in Python programs.

%package -n python2-samba-test
Summary:        Samba Python libraries
Requires:       python2-%{name} = %{samba_depver}

%description -n python2-samba-test
This package contains some python libraries for test package of %{name}.

%package -n python2-samba-dc
Summary:        Python libraries for Samba AD
Requires:       python2-%{name} = %{samba_depver}

%description -n python2-samba-dc
This package contains the Python libraries needed by programs
to manage Samba AD.
%endif

%package -n python3-%{name}
Summary:        Python3 library package for %{name}
Requires:       %{name} = %{samba_depver} %{name}-client = %{samba_depver} %{name}-common = %{samba_depver}
Requires:       python3-talloc python3-tevent python3-tdb python3-ldb python3-dns

%description -n python3-%{name}
This package contains the Python 3 libraries needed by programs
that use SMB, RPC and other Samba provided protocols in Python 3 programs.

%package -n python3-samba-test
Summary:        Test package for python3 binding for %{name}
Requires:       python3-%{name} = %{samba_depver}

%description -n python3-samba-test
This package contains the Python libraries used by the test suite of Samba.
If you want to run full set of Samba tests, you need to install this package.

%if %{with_dc}
%package -n python3-samba-dc
Summary:        The Samba Python libraries for Samba AD
Requires:       python3-%{name} = %{samba_depver}

%description -n python3-samba-dc
This contains the Python libraries needed by programs
to manage Samba AD.
%endif

%package pidl
Summary:        Perl IDL compiler package for %{name}
Requires:       perl(Parse::Yapp) perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch
Provides:       samba4-pidl = %{samba_depver}
Obsoletes:      samba4-pidl < %{samba_depver}

%description pidl
This package contains the Perl IDL compiler used by Samba
and Wireshark to parse IDL and similar protocols.

%package test
Summary:        Testing tools and libraries for Samba servers and clients
Requires:       %{name} = %{samba_depver} %{name}-common = %{samba_depver} %{name}-winbind = %{samba_depver}
Requires:       %{name}-client = %{samba_depver}
%if %with_dc
Requires:       %{name}-dc = %{samba_depver}
%endif
%if %with_libsmbclient
Requires:       libsmbclient = %{samba_depver}
%endif
%if %with_libwbclient
Requires:       libwbclient = %{samba_depver}
%endif
Provides:       samba4-test = %{samba_depver} %{name}-test-libs %{name}-test-devel = %{samba_depver}
Obsoletes:      samba4-test < %{samba_depver} %{name}-test-libs %{name}-test-devel < %{samba_depver}

%description test
%{name}-test provides testing tools for both the server and client
packages of Samba.

%package winbind
Summary:        The winbind package for %{name}
Requires:       %{name}-common = %{samba_depver} %{name}-common-tools = %{samba_depver}
Requires:       %{name}-client = %{samba_depver} %{name}-winbind-modules = %{samba_depver}
Provides:       samba4-winbind = %{samba_depver}
Obsoletes:      samba4-winbind < %{samba_depver}

%description winbind
This package provides the winbind NSS library, and some client
tools.  Winbind enables Linux to be a full member in Windows domains and to use
Windows user and group accounts on Linux.

%package winbind-clients
Summary:        The winbind client package for %{name}
Requires:       %{name}-common = %{samba_depver} %{name}-client = %{samba_depver} %{name}-winbind = %{samba_depver}
%if %with_libwbclient
Requires:       libwbclient = %{samba_depver}
%endif
Provides:       samba4-winbind-clients = %{samba_depver}
Obsoletes:      samba4-winbind-clients < %{samba_depver}

%description winbind-clients
This package contains the wbinfo and ntlm_auth tool.

%package winbind-krb5-locator
Summary:        Winbind krb5 locator package for %{name}
Requires:       chkconfig
%if %with_libwbclient
Requires:       libwbclient = %{samba_depver} %{name}-winbind = %{samba_depver}
%else
Requires:       %{name} = %{samba_depver}
%endif
Provides:       samba4-winbind-krb5-locator = %{samba_depver}
Obsoletes:      samba4-winbind-krb5-locator < %{samba_depver}

%description winbind-krb5-locator
This package is a plugin for the system kerberos library to allow
the local kerberos library to use the same KDC as samba and winbind use

%package winbind-modules
Summary:        The winbind modules for %{name}
Requires:       %{name}-client = %{samba_depver} %{name} = %{samba_depver} pam
%if %with_libwbclient
Requires:       libwbclient = %{samba_depver}
%endif

%description winbind-modules
This package provides the NSS library and a PAM module
necessary to communicate to the Winbind Daemon

%if %with_clustering_support
%package -n ctdb
Summary:        A Clustered Database package based on Samba's Trivial Database (TDB)
Requires:       %{name}-client = %{samba_depver} coreutils psmisc sed tdb-tools gawk
Requires:       procps-ng net-tools ethtool iproute iptables util-linux systemd-units

%description -n ctdb
This package is a cluster implementation of the TDB database used by Samba and other
projects to store temporary data. If an application is already using TDB for
temporary data it is very easy to convert that application to be cluster aware
and use CTDB instead.

%package -n ctdb-tests
Summary:        The test package fors CTDB clustered database
Requires:       %{name}-client = %{samba_depver} ctdb = %{samba_depver}
Recommends:     nc
Provides:       ctdb-devel = %{samba_depver}
Obsoletes:      ctdb-devel < %{samba_depver}

%description -n ctdb-tests
This package contains the test suite for CTDB clustered database.
%endif

%package help
Summary:        Help package for %{name}

%description help
This package contains some man help files for %{name}.

%prep
zcat %{SOURCE0} | gpgv2 --quiet --keyring %{SOURCE2} %{SOURCE1} -
%autosetup -n %{name}-%{version} -p1

%build
%global _talloc_lib ,talloc,pytalloc,pytalloc-util
%global _tevent_lib ,tevent,pytevent
%global _tdb_lib ,tdb,pytdb
%global _ldb_lib ,ldb,pyldb,pyldb-util

%global _talloc_lib ,!talloc,!pytalloc,!pytalloc-util
%global _tevent_lib ,!tevent,!pytevent
%global _tdb_lib ,!tdb,!pytdb
%global _ldb_lib ,!ldb,!pyldb,!pyldb-util

%global _samba_libraries !zlib,!popt%{_talloc_lib}%{_tevent_lib}%{_tdb_lib}%{_ldb_lib}

%global _samba_idmap_modules idmap_ad,idmap_rid,idmap_ldap,idmap_hash,idmap_tdb2
%global _samba_pdb_modules pdb_tdbsam,pdb_ldap,pdb_smbpasswd,pdb_wbc_sam,pdb_samba4
%global _samba_auth_modules auth_wbc,auth_unix,auth_server,auth_script,auth_samba4
%global _samba_vfs_modules vfs_dfs_samba4

%global _samba_modules %{_samba_idmap_modules},%{_samba_pdb_modules},%{_samba_auth_modules},%{_samba_vfs_modules}

%global _libsmbclient %nil
%global _libwbclient %nil

%if ! %with_libsmbclient
%global _libsmbclient smbclient,
%endif

%if ! %with_libwbclient
%global _libwbclient wbclient,
%endif

%global _samba_private_libraries %{_libsmbclient}%{_libwbclient}

export python_LDFLAGS="$(echo %{__global_ldflags} | sed -e 's/-Wl,-z,defs//g')"

export LDFLAGS="%{__global_ldflags} -fuse-ld=gold"

pathfix.py -n -p -i %{__python2} buildtools/bin/waf
export RHEL_ALLOW_PYTHON2_FOR_BUILD=1

export PYTHON=%{__python2}

%configure \
        --enable-fhs \
        --with-piddir=/run \
        --with-sockets-dir=/run/samba \
        --with-modulesdir=%{_libdir}/samba \
        --with-pammodulesdir=%{_libdir}/security \
        --with-lockdir=/var/lib/samba/lock \
        --with-statedir=/var/lib/samba \
        --with-cachedir=/var/lib/samba \
        --disable-rpath-install \
        --with-shared-modules=%{_samba_modules} \
        --bundled-libraries=%{_samba_libraries} \
        --with-pam \
        --with-pie \
        --with-relro \
        --without-fam \
%if (! %with_libsmbclient) || (! %with_libwbclient)
        --private-libraries=%{_samba_private_libraries} \
%endif
%if %with_mitkrb5
        --with-system-mitkrb5 \
        --with-experimental-mit-ad-dc \
%endif
%if ! %with_dc
        --without-ad-dc \
%endif
%if ! %with_vfs_glusterfs
        --disable-glusterfs \
%endif
%if %with_clustering_support
        --with-cluster-support \
%endif
%if %with_profiling
        --with-profiling-data \
%endif
%if %{with testsuite}
        --enable-selftest \
%endif
%if %with_intel_aes_accel
        --accel-aes=intelaesni \
%endif
        --with-systemd \
        --systemd-install-services \
        --with-systemddir=/usr/lib/systemd/system \
        --systemd-smb-extra=%{_systemd_extra} \
        --systemd-nmb-extra=%{_systemd_extra} \
        --systemd-winbind-extra=%{_systemd_extra} \
        --systemd-samba-extra=%{_systemd_extra} \
        --extra-python=%{__python3}

%make_build

%install
rm -rf %{buildroot}

export RHEL_ALLOW_PYTHON2_FOR_BUILD=1
export PYTHON=%{__python2}

%make_install

for i in %{buildroot}%{_bindir} %{buildroot}%{_sbindir} ; do
    find $i \
        ! -name '*.pyc' -a \
        ! -name '*.pyo' -a \
        -type f -exec grep -qsm1 '^#!.*\bpython' {} \; \
        -exec sed -i -e '1 s|^#!.*\bpython[^ ]*|#!%{__python2}|' {} \;
done

filenames=$(echo "
    tests/dcerpc/integer.py
    tests/dcerpc/unix.py
")
for file in $filenames; do
    filename="%{buildroot}/%{python3_sitearch}/samba/$file"
    if python3 -c "with open('$filename') as f: compile(f.read(), '$file', 'exec')"; then
        echo "python3 compilation of $file succeeded unexpectedly"
        exit 1
    else
        echo "python3 compilation of $file failed, removing"
        rm "$filename"
    fi
done

install -dm755 %{buildroot}/usr/{sbin,bin}
install -dm755 %{buildroot}%{_libdir}/{security,pkgconfig}
install -dm755 %{buildroot}/%{_libdir}/samba/{ldb,wbclient}
install -dm755 %{buildroot}/var/lib/samba/{drivers,lock,private,scripts,sysvol,winbindd_privileged}
install -dm755 %{buildroot}/var/log/samba/old
install -dm755 %{buildroot}/var/spool/samba
install -dm755 %{buildroot}/var/run/{samba,winbindd}

mv %{buildroot}/%{_libdir}/libwbclient.so* %{buildroot}/%{_libdir}/samba/wbclient
if [ ! -f %{buildroot}/%{_libdir}/samba/wbclient/libwbclient.so.%{libwbc_alternatives_version} ]
then
    echo "Expected libwbclient version not found, please check if version has changed."
    exit -1
fi

pushd %{buildroot}
touch .%{_libexecdir}/samba/cups_backend_smb

install -dm755 .%{_sysconfdir}/logrotate.d
install -m644 %{SOURCE3} .%{_sysconfdir}/logrotate.d/samba

install -m644 %{SOURCE4} .%{_sysconfdir}/samba/smb.conf
install -m644 %{SOURCE5} .%{_sysconfdir}/samba/smb.conf.example

install -dm755 .%{_sysconfdir}/security
install -m644 %{SOURCE6} .%{_sysconfdir}/security/pam_winbind.conf

install -dm755 .%{_sysconfdir}/pam.d
install -m644 %{SOURCE7} .%{_sysconfdir}/pam.d/samba

echo 127.0.0.1 localhost > .%{_sysconfdir}/samba/lmhosts

install -dm755 .%{_sysconfdir}/openldap/schema
install -m644 %{_builddir}/%{name}-%{version}/examples/LDAP/samba.schema \
        %{buildroot}%{_sysconfdir}/openldap/schema/samba.schema

install -m744 %{_builddir}/%{name}-%{version}/packaging/printing/smbprint \
        %{buildroot}%{_bindir}/smbprint

install -dm755 %{buildroot}%{_tmpfilesdir}
install -m644 %{_builddir}/%{name}-%{version}/packaging/systemd/samba.conf.tmp \
        %{buildroot}%{_tmpfilesdir}/samba.conf
popd

echo "d /run/samba  755 root root" >> %{buildroot}%{_tmpfilesdir}/samba.conf
%if %with_clustering_support
echo "d /run/ctdb 755 root root" >> %{buildroot}%{_tmpfilesdir}/ctdb.conf
%endif

install -dm755 %{buildroot}%{_sysconfdir}/sysconfig
install -m644 packaging/systemd/samba.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/samba
%if %with_clustering_support
cat > %{buildroot}%{_sysconfdir}/sysconfig/ctdb <<EOF
EOF

install -dm755 %{buildroot}%{_sysconfdir}/ctdb
install -m644 ctdb/config/ctdb.conf %{buildroot}%{_sysconfdir}/ctdb/ctdb.conf
%endif

%if %with_clustering_support
install -m644 ctdb/config/ctdb.service %{buildroot}%{_unitdir}
%endif

install -dm755 %{buildroot}%{_sysconfdir}/NetworkManager/dispatcher.d/
install -m755 packaging/NetworkManager/30-winbind-systemd \
            %{buildroot}%{_sysconfdir}/NetworkManager/dispatcher.d/30-winbind

install -dm755 %{buildroot}%{_libdir}/krb5/plugins/libkrb5
touch %{buildroot}%{_libdir}/krb5/plugins/libkrb5/winbind_krb5_locator.so

%if ! %with_dc
for i in \
    %{_libdir}/%{name}/libdfs-server-ad-samba4.so \
    %{_libdir}/%{name}/libdnsserver-common-samba4.so \
    %{_libdir}/%{name}/libdsdb-garbage-collect-tombstones-samba4.so \
    %{_libdir}/%{name}/libscavenge-dns-records-samba4.so \
    %{_mandir}/man8/samba.8 \
    %{_mandir}/man8/samba-tool.8 \
    %{_mandir}/man8/samba-gpupdate.8 \
    %{_libdir}/%{name}/ldb/ildap.so \
    %{_libdir}/%{name}/ldb/ldbsamba_extensions.so \
    %{_unitdir}/samba.service \
    %{python2_sitearch}/%{name}/dcerpc/dnsserver.so \
    %{python2_sitearch}/%{name}/dnsserver.py* \
    %{python2_sitearch}/%{name}/domain_update.py* \
    %{python2_sitearch}/%{name}/dsdb_dns.so \
    %{python2_sitearch}/%{name}/dsdb.so \
    %{python2_sitearch}/%{name}/forest_update.py* \
    %{python2_sitearch}/%{name}/gpclass.py* \
    %{python2_sitearch}/%{name}/gpo.so \
    %{python2_sitearch}/%{name}/gp_sec_ext.py* \
    %{python2_sitearch}/%{name}/kcc/debug.py* \
    %{python2_sitearch}/%{name}/kcc/graph.py* \
    %{python2_sitearch}/%{name}/kcc/graph_utils.py* \
    %{python2_sitearch}/%{name}/kcc/__init__.py* \
    %{python2_sitearch}/%{name}/kcc/kcc_utils.py* \
    %{python2_sitearch}/%{name}/kcc/ldif_import_export.py* \
    %{python2_sitearch}/%{name}/mdb_util.py* \
    %{python2_sitearch}/%{name}/ms_forest_updates_markdown.py* \
    %{python2_sitearch}/%{name}/ms_schema_markdown.py* \
    %{python2_sitearch}/%{name}/provision/backend.py* \
    %{python2_sitearch}/%{name}/provision/common.py* \
    %{python2_sitearch}/%{name}/provision/__init__.py* \
    %{python2_sitearch}/%{name}/provision/kerberos_implementation.py* \
    %{python2_sitearch}/%{name}/provision/kerberos.py* \
    %{python2_sitearch}/%{name}/provision/sambadns.py* \
    %{python2_sitearch}/%{name}/samdb.py* \
    %{python2_sitearch}/%{name}/schema.py* \
    %{python2_sitearch}/%{name}/web_server/__init__.py* \
    %{python3_sitearch}/%{name}/dcerpc/dnsserver.*.so \
    %{python3_sitearch}/%{name}/dnsserver.py \
    %{python3_sitearch}/%{name}/domain_update.py \
    %{python3_sitearch}/%{name}/forest_update.py \
    %{python3_sitearch}/%{name}/kcc/__init__.py \
    %{python3_sitearch}/%{name}/kcc/debug.py \
    %{python3_sitearch}/%{name}/kcc/graph.py \
    %{python3_sitearch}/%{name}/kcc/graph_utils.py \
    %{python3_sitearch}/%{name}/kcc/kcc_utils.py \
    %{python3_sitearch}/%{name}/kcc/ldif_import_export.py \
    %{python3_sitearch}/%{name}/kcc/__pycache__/__init__.*.pyc \
    %{python3_sitearch}/%{name}/kcc/__pycache__/debug.*.pyc \
    %{python3_sitearch}/%{name}/kcc/__pycache__/graph.*.pyc \
    %{python3_sitearch}/%{name}/kcc/__pycache__/graph_utils.*.pyc \
    %{python3_sitearch}/%{name}/kcc/__pycache__/kcc_utils.*.pyc \
    %{python3_sitearch}/%{name}/kcc/__pycache__/ldif_import_export.*.pyc \
    %{python3_sitearch}/%{name}/ms_forest_updates_markdown.py \
    %{python3_sitearch}/%{name}/ms_schema_markdown.py \
    %{python3_sitearch}/%{name}/provision/__init__.py \
    %{python3_sitearch}/%{name}/provision/backend.py \
    %{python3_sitearch}/%{name}/provision/common.py \
    %{python3_sitearch}/%{name}/provision/kerberos_implementation.py \
    %{python3_sitearch}/%{name}/provision/kerberos.py \
    %{python3_sitearch}/%{name}/provision/sambadns.py \
    %{python3_sitearch}/%{name}/provision/__pycache__/__init__.*.pyc \
    %{python3_sitearch}/%{name}/provision/__pycache__/backend.*.pyc \
    %{python3_sitearch}/%{name}/provision/__pycache__/common.*.pyc \
    %{python3_sitearch}/%{name}/provision/__pycache__/kerberos_implementation.*.pyc \
    %{python3_sitearch}/%{name}/provision/__pycache__/kerberos.*.pyc \
    %{python3_sitearch}/%{name}/provision/__pycache__/sambadns.*.pyc \
    %{python3_sitearch}/%{name}/__pycache__/domain_update.*.pyc \
    %{python3_sitearch}/%{name}/__pycache__/forest_update.*.pyc \
    %{python3_sitearch}/%{name}/__pycache__/ms_forest_updates_markdown.*.pyc \
    %{python3_sitearch}/%{name}/__pycache__/ms_schema_markdown.*.pyc \
    %{python3_sitearch}/%{name}/__pycache__/remove_dc.*.pyc \
    %{python3_sitearch}/%{name}/__pycache__/schema.*.pyc \
    %{python3_sitearch}/%{name}/remove_dc.py \
    %{python3_sitearch}/%{name}/samdb.py \
    %{python3_sitearch}/%{name}/schema.py \
    %{_sbindir}/samba-gpupdate \
    ; do
    rm -f %{buildroot}$i
done
%endif

/sbin/ldconfig -N -n %{buildroot}%{_libdir}

find %{buildroot}%{python2_sitearch} -name "*.pyc" -print -delete

%if ! %with_dc
rm -rf %{buildroot}%{python2_sitearch}
for f in samba/libsamba-net-samba4.so \
         samba/libsamba-python-samba4.so \
         libsamba-policy.so* \
         pkgconfig/samba-policy.pc ; do
    rm -f %{buildroot}%{_libdir}/$f
done
%endif

%if %{with testsuite}
%check
export RHEL_ALLOW_PYTHON2_FOR_BUILD=1
export PYTHON=%{__python2}

%make_build test TDB_NO_FSYNC=1
%endif

%post
/sbin/ldconfig
%systemd_post smb.service
%systemd_post nmb.service

%preun
%systemd_preun smb.service
%systemd_preun nmb.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart smb.service
%systemd_postun_with_restart nmb.service

%pre common
getent group printadmin >/dev/null || groupadd -r printadmin || :

%post common
/sbin/ldconfig
%tmpfiles_create %{_tmpfilesdir}/samba.conf
if [ -d /var/cache/samba ]; then
    mv /var/cache/samba/netsamlogon_cache.tdb /var/lib/samba/ 2>/dev/null
    mv /var/cache/samba/winbindd_cache.tdb /var/lib/samba/ 2>/dev/null
    rm -rf /var/cache/samba/
    ln -sf /var/cache/samba /var/lib/samba/
fi

%postun common
/sbin/ldconfig

%post client
/sbin/ldconfig
%{_sbindir}/update-alternatives --install %{_libexecdir}/samba/cups_backend_smb \
    cups_backend_smb \
    %{_bindir}/smbspool 10

%postun client
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    %{_sbindir}/update-alternatives --remove cups_backend_smb %{_bindir}/smbspool
fi

%if %with_dc
%post dc
/sbin/ldconfig
%systemd_post samba.service

%preun dc
%systemd_preun samba.service

%postun dc
/sbin/ldconfig
%systemd_postun_with_restart samba.service
%endif

%post krb5-printing
%{_sbindir}/update-alternatives --install %{_libexecdir}/samba/cups_backend_smb \
    cups_backend_smb \
    %{_libexecdir}/samba/smbspool_krb5_wrapper 50

%postun krb5-printing
if [ $1 -eq 0 ] ; then
    %{_sbindir}/update-alternatives --remove cups_backend_smb %{_libexecdir}/samba/smbspool_krb5_wrapper
fi

%if %with_libsmbclient
%post -n libsmbclient -p /sbin/ldconfig

%postun -n libsmbclient -p /sbin/ldconfig
%endif

%if %with_libwbclient
%posttrans -n libwbclient
%{_sbindir}/update-alternatives \
        --install \
        %{_libdir}/libwbclient.so.%{libwbc_alternatives_version} \
        libwbclient.so.%{libwbc_alternatives_version}%{libwbc_alternatives_suffix} \
        %{_libdir}/samba/wbclient/libwbclient.so.%{libwbc_alternatives_version} \
        10
/sbin/ldconfig

%preun -n libwbclient
%{_sbindir}/update-alternatives \
        --remove \
        libwbclient.so.%{libwbc_alternatives_version}%{libwbc_alternatives_suffix} \
        %{_libdir}/samba/wbclient/libwbclient.so.%{libwbc_alternatives_version}
/sbin/ldconfig

%posttrans -n libwbclient-devel
%{_sbindir}/update-alternatives \
        --install %{_libdir}/libwbclient.so \
        libwbclient.so%{libwbc_alternatives_suffix} \
        %{_libdir}/samba/wbclient/libwbclient.so \
        10

%preun -n libwbclient-devel
if [ "`readlink %{_libdir}/libwbclient.so`" == "libwbclient.so.%{libwbc_alternatives_version}" ]; then
    /bin/rm -f /etc/alternatives/libwbclient.so%{libwbc_alternatives_suffix} /var/lib/alternatives/libwbclient.so%{libwbc_alternatives_suffix} 2> /dev/null
else
    %{_sbindir}/update-alternatives --remove libwbclient.so%{libwbc_alternatives_suffix} %{_libdir}/samba/wbclient/libwbclient.so
fi

%endif

%post test -p /sbin/ldconfig

%postun test -p /sbin/ldconfig

%pre winbind
/usr/sbin/groupadd -g 88 wbpriv >/dev/null 2>&1 || :

%post winbind
%systemd_post winbind.service

%preun winbind
%systemd_preun winbind.service

%postun winbind
%systemd_postun_with_restart smb.service
%systemd_postun_with_restart nmb.service

%postun winbind-krb5-locator
if [ "$1" -ge "1" ]; then
        if [ "`readlink %{_sysconfdir}/alternatives/winbind_krb5_locator.so`" == "%{_libdir}/samba/krb5/winbind_krb5_locator.so" ]; then
                %{_sbindir}/update-alternatives --set winbind_krb5_locator.so %{_libdir}/samba/krb5/winbind_krb5_locator.so
        fi
fi

%post winbind-krb5-locator
%{_sbindir}/update-alternatives --install %{_libdir}/krb5/plugins/libkrb5/winbind_krb5_locator.so \
                                winbind_krb5_locator.so %{_libdir}/samba/krb5/winbind_krb5_locator.so 10

%preun winbind-krb5-locator
if [ $1 -eq 0 ]; then
        %{_sbindir}/update-alternatives --remove winbind_krb5_locator.so %{_libdir}/samba/krb5/winbind_krb5_locator.so
fi

%post winbind-modules -p /sbin/ldconfig

%postun winbind-modules -p /sbin/ldconfig

%if %with_clustering_support
%post -n ctdb
/usr/bin/systemd-tmpfiles --create %{_tmpfilesdir}/ctdb.conf
%systemd_post ctdb.service

%preun -n ctdb
%systemd_preun ctdb.service

%postun -n ctdb
%systemd_postun_with_restart ctdb.service
%endif

%files
%license COPYING
%doc README WHATSNEW.txt
%doc examples/autofs examples/LDAP examples/misc
%doc examples/printer-accounting examples/printing
%{_libdir}/libdcerpc-samr.so.*
%{_libdir}/%{name}/libMESSAGING-samba4.so
%{_libdir}/%{name}/libMESSAGING-SEND-samba4.so
%{_libdir}/%{name}/libLIBWBCLIENT-OLD-samba4.so
%{_libdir}/%{name}/libauth4-samba4.so
%{_libdir}/%{name}/libauth-unix-token-samba4.so
%{_libdir}/%{name}/libcluster-samba4.so
%{_libdir}/%{name}/libdcerpc-samba4.so
%{_libdir}/%{name}/libnon-posix-acls-samba4.so
%{_libdir}/%{name}/libshares-samba4.so
%{_libdir}/%{name}/libsmbpasswdparser-samba4.so
%{_libdir}/%{name}/libxattr-tdb-samba4.so
%{_bindir}/smbstatus
%{_sbindir}/smbd
%{_sbindir}/nmbd
%{_sbindir}/eventlogadm
%if %{with_dc}
%{_libdir}/samba/vfs/dfs_samba4.so
%{_libdir}/samba/libdfs-server-ad-samba4.so
%endif
%dir %{_libdir}/%{name}/auth
%dir %{_libdir}/%{name}/vfs
%{_libdir}/%{name}/auth/script.so
%{_libdir}/%{name}/auth/unix.so
%{_libdir}/%{name}/vfs/acl_tdb.so
%{_libdir}/%{name}/vfs/acl_xattr.so
%{_libdir}/%{name}/vfs/aio_fork.so
%{_libdir}/%{name}/vfs/aio_pthread.so
%{_libdir}/%{name}/vfs/audit.so
%{_libdir}/%{name}/vfs/btrfs.so
%{_libdir}/%{name}/vfs/cap.so
%{_libdir}/%{name}/vfs/catia.so
%{_libdir}/%{name}/vfs/commit.so
%{_libdir}/%{name}/vfs/crossrename.so
%{_libdir}/%{name}/vfs/default_quota.so
%{_libdir}/%{name}/vfs/dirsort.so
%{_libdir}/%{name}/vfs/expand_msdfs.so
%{_libdir}/%{name}/vfs/extd_audit.so
%{_libdir}/%{name}/vfs/fake_perms.so
%{_libdir}/%{name}/vfs/fileid.so
%{_libdir}/%{name}/vfs/fruit.so
%{_libdir}/%{name}/vfs/full_audit.so
%{_libdir}/%{name}/vfs/linux_xfs_sgid.so
%{_libdir}/%{name}/vfs/media_harmony.so
%{_libdir}/%{name}/vfs/netatalk.so
%{_libdir}/%{name}/vfs/offline.so
%{_libdir}/%{name}/vfs/preopen.so
%{_libdir}/%{name}/vfs/readahead.so
%{_libdir}/%{name}/vfs/readonly.so
%{_libdir}/%{name}/vfs/recycle.so
%{_libdir}/%{name}/vfs/shadow_copy.so
%{_libdir}/%{name}/vfs/shadow_copy2.so
%{_libdir}/%{name}/vfs/shell_snap.so
%{_libdir}/%{name}/vfs/snapper.so
%{_libdir}/%{name}/vfs/streams_depot.so
%{_libdir}/%{name}/vfs/streams_xattr.so
%{_libdir}/%{name}/vfs/syncops.so
%{_libdir}/%{name}/vfs/time_audit.so
%{_libdir}/%{name}/vfs/unityed_media.so
%{_libdir}/%{name}/vfs/virusfilter.so
%{_libdir}/%{name}/vfs/worm.so
%{_libdir}/%{name}/vfs/xattr_tdb.so
%{_unitdir}/nmb.service
%{_unitdir}/smb.service
%attr(1777,root,root) %dir /var/spool/samba
%dir %{_sysconfdir}/openldap/schema
%config %{_sysconfdir}/openldap/schema/samba.schema
%config(noreplace) %{_sysconfdir}/pam.d/samba

%if ! %{with_vfs_glusterfs}
%exclude %{_mandir}/man8/vfs_glusterfs.8*
%endif

%if ! %{with_vfs_cephfs}
%exclude %{_mandir}/man8/vfs_ceph.8*
%endif

%attr(775,root,printadmin) %dir /var/lib/samba/drivers

%files client
%{_libdir}/libdcerpc-binding.so.*
%{_libdir}/libndr.so.*
%{_libdir}/libndr-krb5pac.so.*
%{_libdir}/libndr-nbt.so.*
%{_libdir}/libndr-standard.so.*
%{_libdir}/libnetapi.so.*
%{_libdir}/libsamba-credentials.so.*
%{_libdir}/libsamba-errors.so.*
%{_libdir}/libsamba-passdb.so.*
%{_libdir}/libsamba-util.so.*
%{_libdir}/libsamba-hostconfig.so.*
%{_libdir}/libsamdb.so.*
%{_libdir}/libsmbconf.so.*
%{_libdir}/libsmbldap.so.*
%{_libdir}/libtevent-util.so.*
%{_libdir}/libdcerpc.so.*

%{_bindir}/cifsdd
%{_bindir}/dbwrap_tool
%{_bindir}/findsmb
%{_bindir}/mvxattr
%{_bindir}/nmblookup
%{_bindir}/oLschema2ldif
%{_bindir}/reg*
%{_bindir}/rpcclient
%{_bindir}/samba-regedit
%{_bindir}/sharesec
%{_bindir}/smb*
%exclude %{_bindir}/smbcontrol
%exclude %{_bindir}/smbpasswd
%exclude %{_bindir}/smbstatus
%exclude %{_bindir}/smbtorture

%dir %{_libexecdir}/samba
%ghost %{_libexecdir}/samba/cups_backend_smb

%dir %{_libdir}/samba
%{_libdir}/%{name}/libCHARSET3-samba4.so
%{_libdir}/%{name}/libaddns-samba4.so
%{_libdir}/%{name}/libads-samba4.so
%{_libdir}/%{name}/libasn1util-samba4.so
%{_libdir}/%{name}/libauth-samba4.so
%{_libdir}/%{name}/libauthkrb5-samba4.so
%{_libdir}/%{name}/libcli-cldap-samba4.so
%{_libdir}/%{name}/libcli-ldap-common-samba4.so
%{_libdir}/%{name}/libcli-ldap-samba4.so
%{_libdir}/%{name}/libcli-nbt-samba4.so
%{_libdir}/%{name}/libcli-smb-common-samba4.so
%{_libdir}/%{name}/libcli-spoolss-samba4.so
%{_libdir}/%{name}/libcliauth-samba4.so
%{_libdir}/%{name}/libcmdline-credentials-samba4.so
%{_libdir}/%{name}/libcommon-auth-samba4.so
%{_libdir}/%{name}/libctdb-event-client-samba4.so
%{_libdir}/%{name}/libdbwrap-samba4.so
%{_libdir}/%{name}/libdcerpc-samba-samba4.so
%{_libdir}/%{name}/libevents-samba4.so
%{_libdir}/%{name}/libflag-mapping-samba4.so
%{_libdir}/%{name}/libgenrand-samba4.so
%{_libdir}/%{name}/libgensec-samba4.so
%{_libdir}/%{name}/libgpext-samba4.so
%{_libdir}/%{name}/libgse-samba4.so
%{_libdir}/%{name}/libhttp-samba4.so
%{_libdir}/%{name}/libinterfaces-samba4.so
%{_libdir}/%{name}/libiov-buf-samba4.so
%{_libdir}/%{name}/libkrb5samba-samba4.so
%{_libdir}/%{name}/libldbsamba-samba4.so
%{_libdir}/%{name}/liblibcli-lsa3-samba4.so
%{_libdir}/%{name}/liblibcli-netlogon3-samba4.so
%{_libdir}/%{name}/liblibsmb-samba4.so
%{_libdir}/%{name}/libmessages-dgm-samba4.so
%{_libdir}/%{name}/libmessages-util-samba4.so
%{_libdir}/%{name}/libmsghdr-samba4.so
%{_libdir}/%{name}/libmsrpc3-samba4.so
%{_libdir}/%{name}/libndr-samba-samba4.so
%{_libdir}/%{name}/libndr-samba4.so
%{_libdir}/%{name}/libnet-keytab-samba4.so
%{_libdir}/%{name}/libnetif-samba4.so
%{_libdir}/%{name}/libnpa-tstream-samba4.so
%{_libdir}/%{name}/libposix-eadb-samba4.so
%{_libdir}/%{name}/libprinting-migrate-samba4.so
%{_libdir}/%{name}/libreplace-samba4.so
%{_libdir}/%{name}/libregistry-samba4.so
%{_libdir}/%{name}/libsamba-cluster-support-samba4.so
%{_libdir}/%{name}/libsamba-debug-samba4.so
%{_libdir}/%{name}/libsamba-modules-samba4.so
%{_libdir}/%{name}/libsamba-security-samba4.so
%{_libdir}/%{name}/libsamba-sockets-samba4.so
%{_libdir}/%{name}/libsamba3-util-samba4.so
%{_libdir}/%{name}/libsamdb-common-samba4.so
%{_libdir}/%{name}/libsecrets3-samba4.so
%{_libdir}/%{name}/libserver-id-db-samba4.so
%{_libdir}/%{name}/libserver-role-samba4.so
%{_libdir}/%{name}/libsmb-transport-samba4.so
%{_libdir}/%{name}/libsmbclient-raw-samba4.so
%{_libdir}/%{name}/libsmbd-base-samba4.so
%{_libdir}/%{name}/libsmbd-conn-samba4.so
%{_libdir}/%{name}/libsmbd-shim-samba4.so
%{_libdir}/%{name}/libsmbldaphelper-samba4.so
%{_libdir}/%{name}/libsys-rw-samba4.so
%{_libdir}/%{name}/libsocket-blocking-samba4.so
%{_libdir}/%{name}/libtalloc-report-samba4.so
%{_libdir}/%{name}/libtdb-wrap-samba4.so
%{_libdir}/%{name}/libtime-basic-samba4.so
%{_libdir}/%{name}/libtorture-samba4.so
%{_libdir}/%{name}/libtrusts-util-samba4.so
%{_libdir}/%{name}/libutil-cmdline-samba4.so
%{_libdir}/%{name}/libutil-reg-samba4.so
%{_libdir}/%{name}/libutil-setid-samba4.so
%{_libdir}/%{name}/libutil-tdb-samba4.so

%if ! %with_libwbclient
%{_libdir}/samba/libwbclient.so.*
%{_libdir}/samba/libwinbind-client-samba4.so
%endif

%if ! %with_libsmbclient
%{_libdir}/samba/libsmbclient.so.*
%{_mandir}/man7/libsmbclient.7*
%endif

%files common
%{_tmpfilesdir}/samba.conf
%dir %{_sysconfdir}/logrotate.d/
%config(noreplace) %{_sysconfdir}/logrotate.d/samba
%attr(0700,root,root) %dir /var/log/samba
%attr(0700,root,root) %dir /var/log/samba/old
%ghost %dir /var/run/samba
%ghost %dir /var/run/winbindd
%dir /var/lib/samba
%attr(700,root,root) %dir /var/lib/samba/private
%dir /var/lib/samba/lock
%attr(755,root,root) %dir %{_sysconfdir}/samba
%config(noreplace) %{_sysconfdir}/samba/smb.conf
%config(noreplace) %{_sysconfdir}/samba/lmhosts
%{_sysconfdir}/samba/smb.conf.example
%config(noreplace) %{_sysconfdir}/sysconfig/samba
%{_libdir}/samba/libpopt-samba3-samba4.so
%if %{with_intel_aes_accel}
%{_libdir}/samba/libaesni-intel-samba4.so
%endif
%dir %{_libdir}/samba/ldb
%dir %{_libdir}/samba/pdb
%{_libdir}/samba/pdb/ldapsam.so
%{_libdir}/samba/pdb/smbpasswd.so
%{_libdir}/samba/pdb/tdbsam.so

%files common-tools
%{_bindir}/net
%{_bindir}/pdbedit
%{_bindir}/profiles
%{_bindir}/smbcontrol
%{_bindir}/smbpasswd
%{_bindir}/testparm

%files dc
%if %with_dc
%{_libdir}/samba/libdb-glue-samba4.so
%{_libdir}/samba/libprocess-model-samba4.so
%{_libdir}/samba/libservice-samba4.so
%dir %{_libdir}/samba/process_model
%{_libdir}/samba/process_model/prefork.so
%{_libdir}/samba/process_model/standard.so
%dir %{_libdir}/samba/service
%{_libdir}/samba/service/cldap.so
%{_libdir}/samba/service/dcerpc.so
%{_libdir}/samba/service/dns.so
%{_libdir}/samba/service/dns_update.so
%{_libdir}/samba/service/drepl.so
%{_libdir}/samba/service/kcc.so
%{_libdir}/samba/service/kdc.so
%{_libdir}/samba/service/ldap.so
%{_libdir}/samba/service/nbtd.so
%{_libdir}/samba/service/ntp_signd.so
%{_libdir}/samba/service/s3fs.so
%{_libdir}/samba/service/web.so
%{_libdir}/samba/service/winbindd.so
%{_libdir}/samba/service/wrepl.so
%{_libdir}/libdcerpc-server.so.*
%{_libdir}/samba/libdnsserver-common-samba4.so
%{_libdir}/samba/libdsdb-module-samba4.so
%{_libdir}/samba/libdsdb-garbage-collect-tombstones-samba4.so
%{_libdir}/samba/libscavenge-dns-records-samba4.so
%else
%doc packaging/README.dc-libs
%endif
%if %with_dc
%{_unitdir}/samba.service
%{_bindir}/samba-tool
%{_sbindir}/samba*

%{_libdir}/krb5/plugins/kdb/samba.so

%{_libdir}/samba/auth/samba4.so
%{_libdir}/samba/libpac-samba4.so
%dir %{_libdir}/samba/gensec
%{_libdir}/%{name}/gensec/krb5.so
%{_libdir}/%{name}/ldb/acl.so
%{_libdir}/%{name}/ldb/aclread.so
%{_libdir}/%{name}/ldb/anr.so
%{_libdir}/%{name}/ldb/audit_log.so
%{_libdir}/%{name}/ldb/descriptor.so
%{_libdir}/%{name}/ldb/dirsync.so
%{_libdir}/%{name}/ldb/dns_notify.so
%{_libdir}/%{name}/ldb/dsdb_notification.so
%{_libdir}/%{name}/ldb/encrypted_secrets.so
%{_libdir}/%{name}/ldb/extended_dn_in.so
%{_libdir}/%{name}/ldb/extended_dn_out.so
%{_libdir}/%{name}/ldb/extended_dn_store.so
%{_libdir}/%{name}/ldb/group_audit_log.so
%{_libdir}/%{name}/ldb/ildap.so
%{_libdir}/%{name}/ldb/instancetype.so
%{_libdir}/%{name}/ldb/lazy_commit.so
%{_libdir}/%{name}/ldb/ldbsamba_extensions.so
%{_libdir}/%{name}/ldb/linked_attributes.so
%{_libdir}/%{name}/ldb/local_password.so
%{_libdir}/%{name}/ldb/new_partition.so
%{_libdir}/%{name}/ldb/objectclass.so
%{_libdir}/%{name}/ldb/objectclass_attrs.so
%{_libdir}/%{name}/ldb/objectguid.so
%{_libdir}/%{name}/ldb/operational.so
%{_libdir}/%{name}/ldb/partition.so
%{_libdir}/%{name}/ldb/password_hash.so
%{_libdir}/%{name}/ldb/ranged_results.so
%{_libdir}/%{name}/ldb/repl_meta_data.so
%{_libdir}/%{name}/ldb/resolve_oids.so
%{_libdir}/%{name}/ldb/rootdse.so
%{_libdir}/%{name}/ldb/samba3sam.so
%{_libdir}/%{name}/ldb/samba3sid.so
%{_libdir}/%{name}/ldb/samba_dsdb.so
%{_libdir}/%{name}/ldb/samba_secrets.so
%{_libdir}/%{name}/ldb/samldb.so
%{_libdir}/%{name}/ldb/schema_data.so
%{_libdir}/%{name}/ldb/schema_load.so
%{_libdir}/%{name}/ldb/secrets_tdb_sync.so
%{_libdir}/%{name}/ldb/show_deleted.so
%{_libdir}/%{name}/ldb/simple_dn.so
%{_libdir}/%{name}/ldb/simple_ldap_map.so
%{_libdir}/%{name}/ldb/subtree_delete.so
%{_libdir}/%{name}/ldb/subtree_rename.so
%{_libdir}/%{name}/ldb/tombstone_reanimate.so
%{_libdir}/%{name}/ldb/unique_object_sids.so
%{_libdir}/%{name}/ldb/update_keytab.so
%{_libdir}/%{name}/ldb/vlv.so
%{_libdir}/%{name}/ldb/wins_ldb.so
%{_libdir}/%{name}/vfs/posix_eadb.so
%dir /var/lib/samba/sysvol
%{_datadir}/samba/setup
%{_mandir}/man8/samba.8*
%{_mandir}/man8/samba-gpupdate.8*
%{_mandir}/man8/samba-tool.8*
%endif # with_dc

%if %with_dc
%files dc-bind-dlz
%attr(770,root,named) %dir /var/lib/samba/bind-dns
%dir %{_libdir}/samba/bind9
%{_libdir}/%{name}/bind9/dlz_bind9.so
%{_libdir}/%{name}/bind9/dlz_bind9_9.so
%{_libdir}/%{name}/bind9/dlz_bind9_10.so
%{_libdir}/%{name}/bind9/dlz_bind9_11.so
%endif

%files devel
%{_includedir}/samba-4.0/charset.h
%{_includedir}/samba-4.0/core/doserr.h
%{_includedir}/samba-4.0/core/error.h
%{_includedir}/samba-4.0/core/hresult.h
%{_includedir}/samba-4.0/core/ntstatus.h
%{_includedir}/samba-4.0/core/ntstatus_gen.h
%{_includedir}/samba-4.0/core/werror.h
%{_includedir}/samba-4.0/core/werror_gen.h
%{_includedir}/samba-4.0/credentials.h
%{_includedir}/samba-4.0/dcerpc.h
%{_includedir}/samba-4.0/domain_credentials.h
%{_includedir}/samba-4.0/gen_ndr/atsvc.h
%{_includedir}/samba-4.0/gen_ndr/auth.h
%{_includedir}/samba-4.0/gen_ndr/dcerpc.h
%{_includedir}/samba-4.0/gen_ndr/krb5pac.h
%{_includedir}/samba-4.0/gen_ndr/lsa.h
%{_includedir}/samba-4.0/gen_ndr/misc.h
%{_includedir}/samba-4.0/gen_ndr/nbt.h
%{_includedir}/samba-4.0/gen_ndr/drsblobs.h
%{_includedir}/samba-4.0/gen_ndr/drsuapi.h
%{_includedir}/samba-4.0/gen_ndr/ndr_drsblobs.h
%{_includedir}/samba-4.0/gen_ndr/ndr_drsuapi.h
%{_includedir}/samba-4.0/gen_ndr/ndr_atsvc.h
%{_includedir}/samba-4.0/gen_ndr/ndr_dcerpc.h
%{_includedir}/samba-4.0/gen_ndr/ndr_krb5pac.h
%{_includedir}/samba-4.0/gen_ndr/ndr_misc.h
%{_includedir}/samba-4.0/gen_ndr/ndr_nbt.h
%{_includedir}/samba-4.0/gen_ndr/ndr_samr.h
%{_includedir}/samba-4.0/gen_ndr/ndr_samr_c.h
%{_includedir}/samba-4.0/gen_ndr/ndr_svcctl.h
%{_includedir}/samba-4.0/gen_ndr/ndr_svcctl_c.h
%{_includedir}/samba-4.0/gen_ndr/netlogon.h
%{_includedir}/samba-4.0/gen_ndr/samr.h
%{_includedir}/samba-4.0/gen_ndr/security.h
%{_includedir}/samba-4.0/gen_ndr/server_id.h
%{_includedir}/samba-4.0/gen_ndr/svcctl.h
%{_includedir}/samba-4.0/ldb_wrap.h
%{_includedir}/samba-4.0/lookup_sid.h
%{_includedir}/samba-4.0/machine_sid.h
%{_includedir}/samba-4.0/ndr.h
%dir %{_includedir}/samba-4.0/ndr
%{_includedir}/samba-4.0/ndr/ndr_dcerpc.h
%{_includedir}/samba-4.0/ndr/ndr_drsblobs.h
%{_includedir}/samba-4.0/ndr/ndr_drsuapi.h
%{_includedir}/samba-4.0/ndr/ndr_krb5pac.h
%{_includedir}/samba-4.0/ndr/ndr_svcctl.h
%{_includedir}/samba-4.0/ndr/ndr_nbt.h
%{_includedir}/samba-4.0/netapi.h
%{_includedir}/samba-4.0/param.h
%{_includedir}/samba-4.0/passdb.h
%{_includedir}/samba-4.0/policy.h
%{_includedir}/samba-4.0/rpc_common.h
%{_includedir}/samba-4.0/samba/session.h
%{_includedir}/samba-4.0/samba/version.h
%{_includedir}/samba-4.0/share.h
%{_includedir}/samba-4.0/smb2_lease_struct.h
%{_includedir}/samba-4.0/smbconf.h
%{_includedir}/samba-4.0/smb_ldap.h
%{_includedir}/samba-4.0/smbldap.h
%{_includedir}/samba-4.0/tdr.h
%{_includedir}/samba-4.0/tsocket.h
%{_includedir}/samba-4.0/tsocket_internal.h
%dir %{_includedir}/samba-4.0/util
%{_includedir}/samba-4.0/util/attr.h
%{_includedir}/samba-4.0/util/blocking.h
%{_includedir}/samba-4.0/util/byteorder.h
%{_includedir}/samba-4.0/util/data_blob.h
%{_includedir}/samba-4.0/util/debug.h
%{_includedir}/samba-4.0/util/fault.h
%{_includedir}/samba-4.0/util/genrand.h
%{_includedir}/samba-4.0/util/idtree.h
%{_includedir}/samba-4.0/util/idtree_random.h
%{_includedir}/samba-4.0/util/memory.h
%{_includedir}/samba-4.0/util/safe_string.h
%{_includedir}/samba-4.0/util/signal.h
%{_includedir}/samba-4.0/util/string_wrappers.h
%{_includedir}/samba-4.0/util/substitute.h
%{_includedir}/samba-4.0/util/talloc_stack.h
%{_includedir}/samba-4.0/util/tevent_ntstatus.h
%{_includedir}/samba-4.0/util/tevent_unix.h
%{_includedir}/samba-4.0/util/tevent_werror.h
%{_includedir}/samba-4.0/util/time.h
%{_includedir}/samba-4.0/util/tfork.h
%{_includedir}/samba-4.0/util_ldb.h
%{_libdir}/libdcerpc-binding.so
%{_libdir}/libdcerpc-samr.so
%{_libdir}/libdcerpc.so
%{_libdir}/libndr-krb5pac.so
%{_libdir}/libndr-nbt.so
%{_libdir}/libndr-standard.so
%{_libdir}/libndr.so
%{_libdir}/libnetapi.so
%{_libdir}/libsamba-credentials.so
%{_libdir}/libsamba-errors.so
%{_libdir}/libsamba-hostconfig.so
%{_libdir}/libsamba-util.so
%{_libdir}/libsamdb.so
%{_libdir}/libsmbconf.so
%{_libdir}/libtevent-util.so
%{_libdir}/pkgconfig/dcerpc.pc
%{_libdir}/pkgconfig/dcerpc_samr.pc
%{_libdir}/pkgconfig/ndr.pc
%{_libdir}/pkgconfig/ndr_krb5pac.pc
%{_libdir}/pkgconfig/ndr_nbt.pc
%{_libdir}/pkgconfig/ndr_standard.pc
%{_libdir}/pkgconfig/netapi.pc
%{_libdir}/pkgconfig/samba-credentials.pc
%{_libdir}/pkgconfig/samba-hostconfig.pc
%{_libdir}/pkgconfig/samba-util.pc
%{_libdir}/pkgconfig/samdb.pc
%{_libdir}/libsamba-passdb.so
%{_libdir}/libsmbldap.so

%if %with_dc
%{_includedir}/samba-4.0/dcerpc_server.h
%{_libdir}/libdcerpc-server.so
%{_libdir}/pkgconfig/dcerpc_server.pc
%{_libdir}/libsamba-policy.so
%{_libdir}/pkgconfig/samba-policy.pc
%endif

%if ! %with_libsmbclient
%{_includedir}/samba-4.0/libsmbclient.h
%endif

%if ! %with_libwbclient
%{_includedir}/samba-4.0/wbclient.h
%endif

%if %{with_vfs_cephfs}
%files vfs-cephfs
%{_libdir}/samba/vfs/ceph.so
%{_mandir}/man8/vfs_ceph.8*
%endif

%if %{with_vfs_glusterfs}
%files vfs-glusterfs
%{_libdir}/samba/vfs/glusterfs.so
%{_mandir}/man8/vfs_glusterfs.8*
%endif

%files krb5-printing
%attr(0700,root,root) %{_libexecdir}/samba/smbspool_krb5_wrapper

%if %with_libsmbclient
%files -n libsmbclient
%{_libdir}/libsmbclient.so.*

%files -n libsmbclient-devel
%{_includedir}/samba-4.0/libsmbclient.h
%{_libdir}/libsmbclient.so
%{_libdir}/pkgconfig/smbclient.pc
%{_mandir}/man7/libsmbclient.7*
%endif

%if %with_libwbclient
%files -n libwbclient
%{_libdir}/samba/wbclient/libwbclient.so.*
%{_libdir}/samba/libwinbind-client-samba4.so

%files -n libwbclient-devel
%{_includedir}/samba-4.0/wbclient.h
%{_libdir}/samba/wbclient/libwbclient.so
%{_libdir}/pkgconfig/wbclient.pc
%endif

%files pidl
%attr(755,root,root) %{_bindir}/pidl
%dir %{perl_vendorlib}/Parse
%{perl_vendorlib}/Parse/Pidl.pm
%dir %{perl_vendorlib}/Parse/Pidl
%{perl_vendorlib}/Parse/Pidl/CUtil.pm
%{perl_vendorlib}/Parse/Pidl/Samba4.pm
%{perl_vendorlib}/Parse/Pidl/Expr.pm
%{perl_vendorlib}/Parse/Pidl/ODL.pm
%{perl_vendorlib}/Parse/Pidl/Typelist.pm
%{perl_vendorlib}/Parse/Pidl/IDL.pm
%{perl_vendorlib}/Parse/Pidl/Compat.pm
%dir %{perl_vendorlib}/Parse/Pidl/Wireshark
%{perl_vendorlib}/Parse/Pidl/Wireshark/Conformance.pm
%{perl_vendorlib}/Parse/Pidl/Wireshark/NDR.pm
%{perl_vendorlib}/Parse/Pidl/Dump.pm
%dir %{perl_vendorlib}/Parse/Pidl/Samba3
%{perl_vendorlib}/Parse/Pidl/Samba3/ServerNDR.pm
%{perl_vendorlib}/Parse/Pidl/Samba3/ClientNDR.pm
%dir %{perl_vendorlib}/Parse/Pidl/Samba4
%{perl_vendorlib}/Parse/Pidl/Samba4/Header.pm
%dir %{perl_vendorlib}/Parse/Pidl/Samba4/COM
%{perl_vendorlib}/Parse/Pidl/Samba4/COM/Header.pm
%{perl_vendorlib}/Parse/Pidl/Samba4/COM/Proxy.pm
%{perl_vendorlib}/Parse/Pidl/Samba4/COM/Stub.pm
%{perl_vendorlib}/Parse/Pidl/Samba4/Python.pm
%{perl_vendorlib}/Parse/Pidl/Samba4/Template.pm
%dir %{perl_vendorlib}/Parse/Pidl/Samba4/NDR
%{perl_vendorlib}/Parse/Pidl/Samba4/NDR/Server.pm
%{perl_vendorlib}/Parse/Pidl/Samba4/NDR/Client.pm
%{perl_vendorlib}/Parse/Pidl/Samba4/NDR/Parser.pm
%{perl_vendorlib}/Parse/Pidl/Samba4/TDR.pm
%{perl_vendorlib}/Parse/Pidl/NDR.pm
%{perl_vendorlib}/Parse/Pidl/Util.pm

%if %{with_dc}
%files -n python2-%{name}
%{_libdir}/samba/libsamba-python-samba4.so
%{_libdir}/samba/libsamba-net-samba4.so
%{_libdir}/libsamba-policy.so.*

%dir %{python2_sitearch}/samba
%{python2_sitearch}/%{name}/__init__.py*
%{python2_sitearch}/%{name}/_glue.so
%{python2_sitearch}/%{name}/_ldb.so
%{python2_sitearch}/%{name}/auth.so
%{python2_sitearch}/%{name}/colour.py*
%{python2_sitearch}/%{name}/common.py*
%{python2_sitearch}/%{name}/compat.py*
%{python2_sitearch}/%{name}/credentials.so
%{python2_sitearch}/%{name}/crypto.so
%{python2_sitearch}/%{name}/dbchecker.py*
%{python2_sitearch}/%{name}/descriptor.py*
%{python2_sitearch}/%{name}/drs_utils.py*
%{python2_sitearch}/%{name}/gensec.so
%{python2_sitearch}/%{name}/getopt.py*
%{python2_sitearch}/%{name}/graph.py*
%{python2_sitearch}/%{name}/hostconfig.py*
%{python2_sitearch}/%{name}/idmap.py*
%{python2_sitearch}/%{name}/join.py*
%{python2_sitearch}/%{name}/messaging.so
%{python2_sitearch}/%{name}/ms_display_specifiers.py*
%{python2_sitearch}/%{name}/ms_schema.py*
%{python2_sitearch}/%{name}/ndr.py*
%{python2_sitearch}/%{name}/net.so
%{python2_sitearch}/%{name}/netbios.so
%{python2_sitearch}/%{name}/ntacls.py*
%{python2_sitearch}/%{name}/ntstatus.so
%{python2_sitearch}/%{name}/param.so
%{python2_sitearch}/%{name}/policy.so
%{python2_sitearch}/%{name}/posix_eadb.so
%{python2_sitearch}/%{name}/registry.so
%{python2_sitearch}/%{name}/remove_dc.py*
%{python2_sitearch}/%{name}/sd_utils.py*
%{python2_sitearch}/%{name}/security.so
%{python2_sitearch}/%{name}/sites.py*
%{python2_sitearch}/%{name}/smb.so
%{python2_sitearch}/%{name}/subnets.py*
%{python2_sitearch}/%{name}/upgrade.py*
%{python2_sitearch}/%{name}/upgradehelpers.py*
%{python2_sitearch}/%{name}/werror.so
%{python2_sitearch}/%{name}/xattr.py*
%{python2_sitearch}/%{name}/xattr_native.so
%{python2_sitearch}/%{name}/xattr_tdb.so

%dir %{python2_sitearch}/samba/dcerpc
%{python2_sitearch}/%{name}/dcerpc/__init__.py*
%{python2_sitearch}/%{name}/dcerpc/atsvc.so
%{python2_sitearch}/%{name}/dcerpc/auth.so
%{python2_sitearch}/%{name}/dcerpc/base.so
%{python2_sitearch}/%{name}/dcerpc/dcerpc.so
%{python2_sitearch}/%{name}/dcerpc/dfs.so
%{python2_sitearch}/%{name}/dcerpc/dns.so
%{python2_sitearch}/%{name}/dcerpc/dnsp.so
%{python2_sitearch}/%{name}/dcerpc/drsblobs.so
%{python2_sitearch}/%{name}/dcerpc/drsuapi.so
%{python2_sitearch}/%{name}/dcerpc/echo.so
%{python2_sitearch}/%{name}/dcerpc/epmapper.so
%{python2_sitearch}/%{name}/dcerpc/idmap.so
%{python2_sitearch}/%{name}/dcerpc/initshutdown.so
%{python2_sitearch}/%{name}/dcerpc/irpc.so
%{python2_sitearch}/%{name}/dcerpc/krb5pac.so
%{python2_sitearch}/%{name}/dcerpc/lsa.so
%{python2_sitearch}/%{name}/dcerpc/messaging.so
%{python2_sitearch}/%{name}/dcerpc/mgmt.so
%{python2_sitearch}/%{name}/dcerpc/misc.so
%{python2_sitearch}/%{name}/dcerpc/nbt.so
%{python2_sitearch}/%{name}/dcerpc/netlogon.so
%{python2_sitearch}/%{name}/dcerpc/ntlmssp.so
%{python2_sitearch}/%{name}/dcerpc/samr.so
%{python2_sitearch}/%{name}/dcerpc/security.so
%{python2_sitearch}/%{name}/dcerpc/server_id.so
%{python2_sitearch}/%{name}/dcerpc/smb_acl.so
%{python2_sitearch}/%{name}/dcerpc/srvsvc.so
%{python2_sitearch}/%{name}/dcerpc/svcctl.so
%{python2_sitearch}/%{name}/dcerpc/unixinfo.so
%{python2_sitearch}/%{name}/dcerpc/winbind.so
%{python2_sitearch}/%{name}/dcerpc/winreg.so
%{python2_sitearch}/%{name}/dcerpc/wkssvc.so
%{python2_sitearch}/%{name}/dcerpc/xattr.so

%dir %{python2_sitearch}/samba/emulate
%{python2_sitearch}/%{name}/emulate/__init__.py*
%{python2_sitearch}/%{name}/emulate/traffic.py*
%{python2_sitearch}/%{name}/emulate/traffic_packets.py*

%dir %{python2_sitearch}/samba/netcmd
%{python2_sitearch}/%{name}/netcmd/__init__.py*
%{python2_sitearch}/%{name}/netcmd/common.py*
%{python2_sitearch}/%{name}/netcmd/computer.py*
%{python2_sitearch}/%{name}/netcmd/dbcheck.py*
%{python2_sitearch}/%{name}/netcmd/delegation.py*
%{python2_sitearch}/%{name}/netcmd/dns.py*
%{python2_sitearch}/%{name}/netcmd/domain.py*
%{python2_sitearch}/%{name}/netcmd/domain_backup.py*
%{python2_sitearch}/%{name}/netcmd/drs.py*
%{python2_sitearch}/%{name}/netcmd/dsacl.py*
%{python2_sitearch}/%{name}/netcmd/forest.py*
%{python2_sitearch}/%{name}/netcmd/fsmo.py*
%{python2_sitearch}/%{name}/netcmd/gpo.py*
%{python2_sitearch}/%{name}/netcmd/group.py*
%{python2_sitearch}/%{name}/netcmd/ldapcmp.py*
%{python2_sitearch}/%{name}/netcmd/main.py*
%{python2_sitearch}/%{name}/netcmd/nettime.py*
%{python2_sitearch}/%{name}/netcmd/ntacl.py*
%{python2_sitearch}/%{name}/netcmd/ou.py*
%{python2_sitearch}/%{name}/netcmd/processes.py*
%{python2_sitearch}/%{name}/netcmd/pso.py*
%{python2_sitearch}/%{name}/netcmd/rodc.py*
%{python2_sitearch}/%{name}/netcmd/schema.py*
%{python2_sitearch}/%{name}/netcmd/sites.py*
%{python2_sitearch}/%{name}/netcmd/spn.py*
%{python2_sitearch}/%{name}/netcmd/testparm.py*
%{python2_sitearch}/%{name}/netcmd/user.py*
%{python2_sitearch}/%{name}/netcmd/visualize.py*

%dir %{python2_sitearch}/samba/samba3
%{python2_sitearch}/%{name}/samba3/__init__.py*
%{python2_sitearch}/%{name}/samba3/libsmb_samba_internal.so
%{python2_sitearch}/%{name}/samba3/param.so
%{python2_sitearch}/%{name}/samba3/passdb.so
%{python2_sitearch}/%{name}/samba3/smbd.so

%dir %{python2_sitearch}/samba/subunit
%{python2_sitearch}/%{name}/subunit/__init__.py*
%{python2_sitearch}/%{name}/subunit/run.py*
%{python2_sitearch}/%{name}/tdb_util.py*

%dir %{python2_sitearch}/samba/third_party
%{python2_sitearch}/samba/third_party/__init__.py*

%if %{with_dc}
%files -n python2-%{name}-dc
%{python2_sitearch}/%{name}/domain_update.py*
%{python2_sitearch}/%{name}/dckeytab.so
%{python2_sitearch}/%{name}/dsdb.so
%{python2_sitearch}/%{name}/dsdb_dns.so
%{python2_sitearch}/%{name}/dnsserver.py*
%{python2_sitearch}/%{name}/forest_update.py*
%{python2_sitearch}/%{name}/gpclass.py*
%{python2_sitearch}/%{name}/gpo.so
%{python2_sitearch}/%{name}/gp_sec_ext.py*
%{python2_sitearch}/%{name}/mdb_util.py*
%{python2_sitearch}/%{name}/ms_forest_updates_markdown.py*
%{python2_sitearch}/%{name}/ms_schema_markdown.py*
%{python2_sitearch}/%{name}/samdb.py*
%{python2_sitearch}/%{name}/schema.py*

%{python2_sitearch}/%{name}/dcerpc/dnsserver.so

%dir %{python2_sitearch}/samba/kcc
%{python2_sitearch}/%{name}/kcc/__init__.py*
%{python2_sitearch}/%{name}/kcc/debug.py*
%{python2_sitearch}/%{name}/kcc/graph.py*
%{python2_sitearch}/%{name}/kcc/graph_utils.py*
%{python2_sitearch}/%{name}/kcc/kcc_utils.py*
%{python2_sitearch}/%{name}/kcc/ldif_import_export.py*

%dir %{python2_sitearch}/samba/provision
%{python2_sitearch}/%{name}/provision/__init__.py*
%{python2_sitearch}/%{name}/provision/backend.py*
%{python2_sitearch}/%{name}/provision/common.py*
%{python2_sitearch}/%{name}/provision/kerberos.py*
%{python2_sitearch}/%{name}/provision/kerberos_implementation.py*
%{python2_sitearch}/%{name}/provision/sambadns.py*

%dir %{python2_sitearch}/samba/web_server
%{python2_sitearch}/samba/web_server/__init__.py*
%endif

%files -n python2-%{name}-test
%dir %{python2_sitearch}/samba/tests
%{python2_sitearch}/%{name}/tests/__init__.py*
%{python2_sitearch}/%{name}/tests/audit_log_base.py*
%{python2_sitearch}/%{name}/tests/audit_log_dsdb.py*
%{python2_sitearch}/%{name}/tests/audit_log_pass_change.py*
%{python2_sitearch}/%{name}/tests/auth.py*
%{python2_sitearch}/%{name}/tests/auth_log.py*
%{python2_sitearch}/%{name}/tests/auth_log_base.py*
%{python2_sitearch}/%{name}/tests/auth_log_ncalrpc.py*
%{python2_sitearch}/%{name}/tests/auth_log_netlogon.py*
%{python2_sitearch}/%{name}/tests/auth_log_netlogon_bad_creds.py*
%{python2_sitearch}/%{name}/tests/auth_log_pass_change.py*
%{python2_sitearch}/%{name}/tests/auth_log_samlogon.py*
%dir %{python2_sitearch}/samba/tests/blackbox
%{python2_sitearch}/%{name}/tests/blackbox/__init__.py*
%{python2_sitearch}/%{name}/tests/blackbox/check_output.py*
%{python2_sitearch}/%{name}/tests/blackbox/ndrdump.py*
%{python2_sitearch}/%{name}/tests/blackbox/samba_dnsupdate.py*
%{python2_sitearch}/%{name}/tests/blackbox/smbcontrol.py*
%{python2_sitearch}/%{name}/tests/blackbox/traffic_learner.py*
%{python2_sitearch}/%{name}/tests/blackbox/traffic_replay.py*
%{python2_sitearch}/%{name}/tests/blackbox/traffic_summary.py*
%{python2_sitearch}/%{name}/tests/common.py*
%{python2_sitearch}/%{name}/tests/core.py*
%{python2_sitearch}/%{name}/tests/credentials.py*
%dir %{python2_sitearch}/samba/tests/dcerpc
%{python2_sitearch}/%{name}/tests/dcerpc/__init__.py*
%{python2_sitearch}/%{name}/tests/dcerpc/array.py*
%{python2_sitearch}/%{name}/tests/dcerpc/bare.py*
%{python2_sitearch}/%{name}/tests/dcerpc/dnsserver.py*
%{python2_sitearch}/%{name}/tests/dcerpc/integer.py*
%{python2_sitearch}/%{name}/tests/dcerpc/misc.py*
%{python2_sitearch}/%{name}/tests/dcerpc/raw_protocol.py*
%{python2_sitearch}/%{name}/tests/dcerpc/raw_testcase.py*
%{python2_sitearch}/%{name}/tests/dcerpc/registry.py*
%{python2_sitearch}/%{name}/tests/dcerpc/rpc_talloc.py*
%{python2_sitearch}/%{name}/tests/dcerpc/rpcecho.py*
%{python2_sitearch}/%{name}/tests/dcerpc/sam.py*
%{python2_sitearch}/%{name}/tests/dcerpc/srvsvc.py*
%{python2_sitearch}/%{name}/tests/dcerpc/string.py*
%{python2_sitearch}/%{name}/tests/dcerpc/testrpc.py*
%{python2_sitearch}/%{name}/tests/dcerpc/unix.py*
%{python2_sitearch}/%{name}/tests/dckeytab.py*
%{python2_sitearch}/%{name}/tests/dns.py*
%{python2_sitearch}/%{name}/tests/dns_base.py*
%{python2_sitearch}/%{name}/tests/dns_forwarder.py*
%{python2_sitearch}/%{name}/tests/dns_invalid.py*
%dir %{python2_sitearch}/samba/tests/dns_forwarder_helpers
%{python2_sitearch}/%{name}/tests/dns_forwarder_helpers/server.py*
%{python2_sitearch}/%{name}/tests/dns_tkey.py*
%{python2_sitearch}/%{name}/tests/dns_wildcard.py*
%{python2_sitearch}/%{name}/tests/docs.py*
%{python2_sitearch}/%{name}/tests/domain_backup.py*
%{python2_sitearch}/%{name}/tests/dsdb.py*
%{python2_sitearch}/%{name}/tests/dsdb_lock.py*
%{python2_sitearch}/%{name}/tests/dsdb_schema_attributes.py*
%dir %{python2_sitearch}/samba/tests/emulate
%{python2_sitearch}/%{name}/tests/emulate/__init__.py*
%{python2_sitearch}/%{name}/tests/emulate/traffic.py*
%{python2_sitearch}/%{name}/tests/emulate/traffic_packet.py*
%{python2_sitearch}/%{name}/tests/encrypted_secrets.py*
%{python2_sitearch}/%{name}/tests/gensec.py*
%{python2_sitearch}/%{name}/tests/getdcname.py*
%{python2_sitearch}/%{name}/tests/get_opt.py*
%{python2_sitearch}/%{name}/tests/glue.py*
%{python2_sitearch}/%{name}/tests/gpo.py*
%{python2_sitearch}/%{name}/tests/graph.py*
%{python2_sitearch}/%{name}/tests/group_audit.py*
%{python2_sitearch}/%{name}/tests/hostconfig.py*
%{python2_sitearch}/%{name}/tests/join.py*
%dir %{python2_sitearch}/samba/tests/kcc
%{python2_sitearch}/%{name}/tests/kcc/__init__.py*
%{python2_sitearch}/%{name}/tests/kcc/graph.py*
%{python2_sitearch}/%{name}/tests/kcc/graph_utils.py*
%{python2_sitearch}/%{name}/tests/kcc/kcc_utils.py*
%{python2_sitearch}/%{name}/tests/kcc/ldif_import_export.py*
%{python2_sitearch}/%{name}/tests/krb5_credentials.py*
%{python2_sitearch}/%{name}/tests/libsmb_samba_internal.py*
%{python2_sitearch}/%{name}/tests/loadparm.py*
%{python2_sitearch}/%{name}/tests/lsa_string.py*
%{python2_sitearch}/%{name}/tests/messaging.py*
%{python2_sitearch}/%{name}/tests/net_join.py*
%{python2_sitearch}/%{name}/tests/net_join_no_spnego.py*
%{python2_sitearch}/%{name}/tests/netbios.py*
%{python2_sitearch}/%{name}/tests/netcmd.py*
%{python2_sitearch}/%{name}/tests/netlogonsvc.py*
%{python2_sitearch}/%{name}/tests/ntacls.py*
%{python2_sitearch}/%{name}/tests/ntacls_backup.py*
%{python2_sitearch}/%{name}/tests/ntlmdisabled.py*
%{python2_sitearch}/%{name}/tests/pam_winbind.py*
%{python2_sitearch}/%{name}/tests/pam_winbind_warn_pwd_expire.py*
%{python2_sitearch}/%{name}/tests/param.py*
%{python2_sitearch}/%{name}/tests/password_hash.py*
%{python2_sitearch}/%{name}/tests/password_hash_fl2003.py*
%{python2_sitearch}/%{name}/tests/password_hash_fl2008.py*
%{python2_sitearch}/%{name}/tests/password_hash_gpgme.py*
%{python2_sitearch}/%{name}/tests/password_hash_ldap.py*
%{python2_sitearch}/%{name}/tests/password_quality.py*
%{python2_sitearch}/%{name}/tests/password_test.py*
%{python2_sitearch}/%{name}/tests/policy.py*
%{python2_sitearch}/%{name}/tests/posixacl.py*
%{python2_sitearch}/%{name}/tests/provision.py*
%{python2_sitearch}/%{name}/tests/pso.py*
%{python2_sitearch}/%{name}/tests/py_credentials.py*
%{python2_sitearch}/%{name}/tests/registry.py*
%{python2_sitearch}/%{name}/tests/s3idmapdb.py*
%{python2_sitearch}/%{name}/tests/s3param.py*
%{python2_sitearch}/%{name}/tests/s3passdb.py*
%{python2_sitearch}/%{name}/tests/s3registry.py*
%{python2_sitearch}/%{name}/tests/s3windb.py*
%{python2_sitearch}/%{name}/tests/samba3sam.py*
%dir %{python2_sitearch}/samba/tests/samba_tool
%{python2_sitearch}/%{name}/tests/samba_tool/__init__.py*
%{python2_sitearch}/%{name}/tests/samba_tool/base.py*
%{python2_sitearch}/%{name}/tests/samba_tool/computer.py*
%{python2_sitearch}/%{name}/tests/samba_tool/demote.py*
%{python2_sitearch}/%{name}/tests/samba_tool/dnscmd.py*
%{python2_sitearch}/%{name}/tests/samba_tool/forest.py*
%{python2_sitearch}/%{name}/tests/samba_tool/fsmo.py*
%{python2_sitearch}/%{name}/tests/samba_tool/gpo.py*
%{python2_sitearch}/%{name}/tests/samba_tool/group.py*
%{python2_sitearch}/%{name}/tests/samba_tool/help.py*
%{python2_sitearch}/%{name}/tests/samba_tool/join.py*
%{python2_sitearch}/%{name}/tests/samba_tool/ntacl.py*
%{python2_sitearch}/%{name}/tests/samba_tool/ou.py*
%{python2_sitearch}/%{name}/tests/samba_tool/passwordsettings.py*
%{python2_sitearch}/%{name}/tests/samba_tool/processes.py*
%{python2_sitearch}/%{name}/tests/samba_tool/provision_password_check.py*
%{python2_sitearch}/%{name}/tests/samba_tool/rodc.py*
%{python2_sitearch}/%{name}/tests/samba_tool/schema.py*
%{python2_sitearch}/%{name}/tests/samba_tool/sites.py*
%{python2_sitearch}/%{name}/tests/samba_tool/timecmd.py*
%{python2_sitearch}/%{name}/tests/samba_tool/user.py*
%{python2_sitearch}/%{name}/tests/samba_tool/user_check_password_script.py*
%{python2_sitearch}/%{name}/tests/samba_tool/user_virtualCryptSHA.py*
%{python2_sitearch}/%{name}/tests/samba_tool/user_wdigest.py*
%{python2_sitearch}/%{name}/tests/samba_tool/visualize.py*
%{python2_sitearch}/%{name}/tests/samba_tool/visualize_drs.py*
%{python2_sitearch}/%{name}/tests/samdb.py*
%{python2_sitearch}/%{name}/tests/samdb_api.py*
%{python2_sitearch}/%{name}/tests/security.py*
%{python2_sitearch}/%{name}/tests/smb.py*
%{python2_sitearch}/%{name}/tests/source.py*
%{python2_sitearch}/%{name}/tests/strings.py*
%{python2_sitearch}/%{name}/tests/subunitrun.py*
%{python2_sitearch}/%{name}/tests/tdb_util.py*
%{python2_sitearch}/%{name}/tests/unicodenames.py*
%{python2_sitearch}/%{name}/tests/upgrade.py*
%{python2_sitearch}/%{name}/tests/upgradeprovision.py*
%{python2_sitearch}/%{name}/tests/upgradeprovisionneeddc.py*
%{python2_sitearch}/%{name}/tests/xattr.py*
%{python2_sitearch}/%{name}/tests/smbd_base.py*
%endif

%files -n python3-%{name}
%dir %{python3_sitearch}/samba/
%{python3_sitearch}/samba/__init__.py
%dir %{python3_sitearch}/samba/__pycache__
%{python3_sitearch}/%{name}/__pycache__/__init__.*.pyc
%{python3_sitearch}/%{name}/__pycache__/colour.*.pyc
%{python3_sitearch}/%{name}/__pycache__/common.*.pyc
%{python3_sitearch}/%{name}/__pycache__/compat.*.pyc
%{python3_sitearch}/%{name}/__pycache__/dbchecker.*.pyc
%{python3_sitearch}/%{name}/__pycache__/descriptor.*.pyc
%{python3_sitearch}/%{name}/__pycache__/drs_utils.*.pyc
%{python3_sitearch}/%{name}/__pycache__/getopt.*.pyc
%{python3_sitearch}/%{name}/__pycache__/gpclass.*.pyc
%{python3_sitearch}/%{name}/__pycache__/gp_sec_ext.*.pyc
%{python3_sitearch}/%{name}/__pycache__/graph.*.pyc
%{python3_sitearch}/%{name}/__pycache__/hostconfig.*.pyc
%{python3_sitearch}/%{name}/__pycache__/idmap.*.pyc
%{python3_sitearch}/%{name}/__pycache__/join.*.pyc
%{python3_sitearch}/%{name}/__pycache__/mdb_util.*.pyc
%{python3_sitearch}/%{name}/__pycache__/ms_display_specifiers.*.pyc
%{python3_sitearch}/%{name}/__pycache__/ms_schema.*.pyc
%{python3_sitearch}/%{name}/__pycache__/ndr.*.pyc
%{python3_sitearch}/%{name}/__pycache__/ntacls.*.pyc
%{python3_sitearch}/%{name}/__pycache__/sd_utils.*.pyc
%{python3_sitearch}/%{name}/__pycache__/sites.*.pyc
%{python3_sitearch}/%{name}/__pycache__/subnets.*.pyc
%{python3_sitearch}/%{name}/__pycache__/tdb_util.*.pyc
%{python3_sitearch}/%{name}/__pycache__/upgrade.*.pyc
%{python3_sitearch}/%{name}/__pycache__/upgradehelpers.*.pyc
%{python3_sitearch}/%{name}/__pycache__/xattr.*.pyc
%{python3_sitearch}/%{name}/_glue.*.so
%{python3_sitearch}/%{name}/_ldb.*.so
%{python3_sitearch}/%{name}/auth.*.so
%{python3_sitearch}/%{name}/dbchecker.py
%{python3_sitearch}/%{name}/colour.py
%{python3_sitearch}/%{name}/common.py
%{python3_sitearch}/%{name}/compat.py
%{python3_sitearch}/%{name}/credentials.*.so
%{python3_sitearch}/%{name}/crypto.*.so
%dir %{python3_sitearch}/samba/dcerpc
%dir %{python3_sitearch}/samba/dcerpc/__pycache__
%{python3_sitearch}/%{name}/dcerpc/__pycache__/__init__.*.pyc
%{python3_sitearch}/%{name}/dcerpc/__init__.py
%{python3_sitearch}/%{name}/dcerpc/atsvc.*.so
%{python3_sitearch}/%{name}/dcerpc/auth.*.so
%{python3_sitearch}/%{name}/dcerpc/base.*.so
%{python3_sitearch}/%{name}/dcerpc/dcerpc.*.so
%{python3_sitearch}/%{name}/dcerpc/dfs.*.so
%{python3_sitearch}/%{name}/dcerpc/dns.*.so
%{python3_sitearch}/%{name}/dcerpc/dnsp.*.so
%{python3_sitearch}/%{name}/dcerpc/drsblobs.*.so
%{python3_sitearch}/%{name}/dcerpc/drsuapi.*.so
%{python3_sitearch}/%{name}/dcerpc/echo.*.so
%{python3_sitearch}/%{name}/dcerpc/epmapper.*.so
%{python3_sitearch}/%{name}/dcerpc/idmap.*.so
%{python3_sitearch}/%{name}/dcerpc/initshutdown.*.so
%{python3_sitearch}/%{name}/dcerpc/irpc.*.so
%{python3_sitearch}/%{name}/dcerpc/krb5pac.*.so
%{python3_sitearch}/%{name}/dcerpc/lsa.*.so
%{python3_sitearch}/%{name}/dcerpc/messaging.*.so
%{python3_sitearch}/%{name}/dcerpc/mgmt.*.so
%{python3_sitearch}/%{name}/dcerpc/misc.*.so
%{python3_sitearch}/%{name}/dcerpc/nbt.*.so
%{python3_sitearch}/%{name}/dcerpc/netlogon.*.so
%{python3_sitearch}/%{name}/dcerpc/ntlmssp.*.so
%{python3_sitearch}/%{name}/dcerpc/samr.*.so
%{python3_sitearch}/%{name}/dcerpc/security.*.so
%{python3_sitearch}/%{name}/dcerpc/server_id.*.so
%{python3_sitearch}/%{name}/dcerpc/smb_acl.*.so
%{python3_sitearch}/%{name}/dcerpc/srvsvc.*.so
%{python3_sitearch}/%{name}/dcerpc/svcctl.*.so
%{python3_sitearch}/%{name}/dcerpc/unixinfo.*.so
%{python3_sitearch}/%{name}/dcerpc/winbind.*.so
%{python3_sitearch}/%{name}/dcerpc/winreg.*.so
%{python3_sitearch}/%{name}/dcerpc/wkssvc.*.so
%{python3_sitearch}/%{name}/dcerpc/xattr.*.so
%{python3_sitearch}/%{name}/descriptor.py
%{python3_sitearch}/%{name}/drs_utils.py
%{python3_sitearch}/%{name}/gensec.*.so
%{python3_sitearch}/%{name}/getopt.py
%{python3_sitearch}/%{name}/gpclass.py
%{python3_sitearch}/%{name}/gp_sec_ext.py
%{python3_sitearch}/%{name}/gpo.*.so
%{python3_sitearch}/%{name}/graph.py
%{python3_sitearch}/%{name}/hostconfig.py
%{python3_sitearch}/%{name}/idmap.py
%{python3_sitearch}/%{name}/join.py
%{python3_sitearch}/%{name}/messaging.*.so
%{python3_sitearch}/%{name}/ndr.py
%{python3_sitearch}/%{name}/net.*.so
%{python3_sitearch}/%{name}/ntstatus.*.so
%{python3_sitearch}/%{name}/posix_eadb.*.so
%dir %{python3_sitearch}/samba/emulate
%dir %{python3_sitearch}/samba/emulate/__pycache__
%{python3_sitearch}/%{name}/emulate/__pycache__/__init__.*.pyc
%{python3_sitearch}/%{name}/emulate/__pycache__/traffic.*.pyc
%{python3_sitearch}/%{name}/emulate/__pycache__/traffic_packets.*.pyc
%{python3_sitearch}/%{name}/emulate/__init__.py
%{python3_sitearch}/%{name}/emulate/traffic.py
%{python3_sitearch}/%{name}/emulate/traffic_packets.py
%{python3_sitearch}/%{name}/mdb_util.py
%{python3_sitearch}/%{name}/ms_display_specifiers.py
%{python3_sitearch}/%{name}/ms_schema.py
%{python3_sitearch}/%{name}/netbios.*.so
%dir %{python3_sitearch}/samba/netcmd
%{python3_sitearch}/samba/netcmd/__init__.py
%dir %{python3_sitearch}/samba/netcmd/__pycache__
%{python3_sitearch}/%{name}/netcmd/__pycache__/__init__.*.pyc
%{python3_sitearch}/%{name}/netcmd/__pycache__/common.*.pyc
%{python3_sitearch}/%{name}/netcmd/__pycache__/computer.*.pyc
%{python3_sitearch}/%{name}/netcmd/__pycache__/dbcheck.*.pyc
%{python3_sitearch}/%{name}/netcmd/__pycache__/delegation.*.pyc
%{python3_sitearch}/%{name}/netcmd/__pycache__/dns.*.pyc
%{python3_sitearch}/%{name}/netcmd/__pycache__/domain.*.pyc
%{python3_sitearch}/%{name}/netcmd/__pycache__/domain_backup.*.pyc
%{python3_sitearch}/%{name}/netcmd/__pycache__/drs.*.pyc
%{python3_sitearch}/%{name}/netcmd/__pycache__/dsacl.*.pyc
%{python3_sitearch}/%{name}/netcmd/__pycache__/forest.*.pyc
%{python3_sitearch}/%{name}/netcmd/__pycache__/fsmo.*.pyc
%{python3_sitearch}/%{name}/netcmd/__pycache__/gpo.*.pyc
%{python3_sitearch}/%{name}/netcmd/__pycache__/group.*.pyc
%{python3_sitearch}/%{name}/netcmd/__pycache__/ldapcmp.*.pyc
%{python3_sitearch}/%{name}/netcmd/__pycache__/main.*.pyc
%{python3_sitearch}/%{name}/netcmd/__pycache__/nettime.*.pyc
%{python3_sitearch}/%{name}/netcmd/__pycache__/ntacl.*.pyc
%{python3_sitearch}/%{name}/netcmd/__pycache__/ou.*.pyc
%{python3_sitearch}/%{name}/netcmd/__pycache__/processes.*.pyc
%{python3_sitearch}/%{name}/netcmd/__pycache__/pso.*.pyc
%{python3_sitearch}/%{name}/netcmd/__pycache__/rodc.*.pyc
%{python3_sitearch}/%{name}/netcmd/__pycache__/schema.*.pyc
%{python3_sitearch}/%{name}/netcmd/__pycache__/sites.*.pyc
%{python3_sitearch}/%{name}/netcmd/__pycache__/spn.*.pyc
%{python3_sitearch}/%{name}/netcmd/__pycache__/testparm.*.pyc
%{python3_sitearch}/%{name}/netcmd/__pycache__/user.*.pyc
%{python3_sitearch}/%{name}/netcmd/__pycache__/visualize.*.pyc
%{python3_sitearch}/%{name}/netcmd/common.py
%{python3_sitearch}/%{name}/netcmd/computer.py
%{python3_sitearch}/%{name}/netcmd/dbcheck.py
%{python3_sitearch}/%{name}/netcmd/delegation.py
%{python3_sitearch}/%{name}/netcmd/dns.py
%{python3_sitearch}/%{name}/netcmd/domain.py
%{python3_sitearch}/%{name}/netcmd/domain_backup.py
%{python3_sitearch}/%{name}/netcmd/drs.py
%{python3_sitearch}/%{name}/netcmd/dsacl.py
%{python3_sitearch}/%{name}/netcmd/forest.py
%{python3_sitearch}/%{name}/netcmd/fsmo.py
%{python3_sitearch}/%{name}/netcmd/gpo.py
%{python3_sitearch}/%{name}/netcmd/group.py
%{python3_sitearch}/%{name}/netcmd/ldapcmp.py
%{python3_sitearch}/%{name}/netcmd/main.py
%{python3_sitearch}/%{name}/netcmd/nettime.py
%{python3_sitearch}/%{name}/netcmd/ntacl.py
%{python3_sitearch}/%{name}/netcmd/ou.py
%{python3_sitearch}/%{name}/netcmd/processes.py
%{python3_sitearch}/%{name}/netcmd/pso.py
%{python3_sitearch}/%{name}/netcmd/rodc.py
%{python3_sitearch}/%{name}/netcmd/schema.py
%{python3_sitearch}/%{name}/netcmd/sites.py
%{python3_sitearch}/%{name}/netcmd/spn.py
%{python3_sitearch}/%{name}/netcmd/testparm.py
%{python3_sitearch}/%{name}/netcmd/user.py
%{python3_sitearch}/%{name}/netcmd/visualize.py
%{python3_sitearch}/%{name}/ntacls.py
%{python3_sitearch}/%{name}/param.*.so
%{python3_sitearch}/%{name}/policy.*.so
%{python3_sitearch}/%{name}/registry.*.so
%{python3_sitearch}/%{name}/security.*.so
%dir %{python3_sitearch}/samba/samba3
%{python3_sitearch}/samba/samba3/__init__.py
%dir %{python3_sitearch}/samba/samba3/__pycache__
%{python3_sitearch}/%{name}/samba3/__pycache__/__init__.*.pyc
%{python3_sitearch}/%{name}/samba3/libsmb_samba_internal.*.so
%{python3_sitearch}/%{name}/samba3/param.*.so
%{python3_sitearch}/%{name}/samba3/passdb.*.so
%{python3_sitearch}/%{name}/samba3/smbd.*.so
%{python3_sitearch}/%{name}/sd_utils.py
%{python3_sitearch}/%{name}/sites.py
%{python3_sitearch}/%{name}/smb.*.so
%{python3_sitearch}/%{name}/subnets.py
%dir %{python3_sitearch}/samba/subunit
%{python3_sitearch}/samba/subunit/__init__.py
%dir %{python3_sitearch}/samba/subunit/__pycache__
%{python3_sitearch}/%{name}/subunit/__pycache__/__init__.*.pyc
%{python3_sitearch}/%{name}/subunit/__pycache__/run.*.pyc
%{python3_sitearch}/%{name}/subunit/run.py
%{python3_sitearch}/%{name}/tdb_util.py
%{python3_sitearch}/%{name}/upgrade.py
%{python3_sitearch}/%{name}/upgradehelpers.py
%{_libdir}/libsamba-policy.*.so*
%{_libdir}/pkgconfig/samba-policy.*.pc
%{_libdir}/samba/libsamba-net.*-samba4.so
%{_libdir}/samba/libsamba-python.*-samba4.so

%if %{with_dc}
%files -n python3-%{name}-dc
%{python3_sitearch}/%{name}/samdb.py
%{python3_sitearch}/%{name}/schema.py
%{python3_sitearch}/%{name}/__pycache__/domain_update.*.pyc
%{python3_sitearch}/%{name}/__pycache__/dnsserver.*.pyc
%{python3_sitearch}/%{name}/__pycache__/forest_update.*.pyc
%{python3_sitearch}/%{name}/__pycache__/ms_forest_updates_markdown.*.pyc
%{python3_sitearch}/%{name}/__pycache__/ms_schema_markdown.*.pyc
%{python3_sitearch}/%{name}/__pycache__/remove_dc.*.pyc
%{python3_sitearch}/%{name}/__pycache__/samdb.*.pyc
%{python3_sitearch}/%{name}/__pycache__/schema.*.pyc
%{python3_sitearch}/%{name}/dcerpc/dnsserver.*.so
%{python3_sitearch}/%{name}/dckeytab.*.so
%{python3_sitearch}/%{name}/dsdb.*.so
%{python3_sitearch}/%{name}/dsdb_dns.*.so
%{python3_sitearch}/%{name}/domain_update.py
%{python3_sitearch}/%{name}/forest_update.py
%{python3_sitearch}/%{name}/ms_forest_updates_markdown.py
%{python3_sitearch}/%{name}/ms_schema_markdown.py

%dir %{python3_sitearch}/samba/kcc
%{python3_sitearch}/%{name}/kcc/__init__.py
%{python3_sitearch}/%{name}/kcc/debug.py
%{python3_sitearch}/%{name}/kcc/graph.py
%{python3_sitearch}/%{name}/kcc/graph_utils.py
%{python3_sitearch}/%{name}/kcc/kcc_utils.py
%{python3_sitearch}/%{name}/kcc/ldif_import_export.py
%{python3_sitearch}/%{name}/dnsserver.py

%dir %{python3_sitearch}/samba/kcc/__pycache__
%{python3_sitearch}/%{name}/kcc/__pycache__/__init__.*.pyc
%{python3_sitearch}/%{name}/kcc/__pycache__/debug.*.pyc
%{python3_sitearch}/%{name}/kcc/__pycache__/graph.*.pyc
%{python3_sitearch}/%{name}/kcc/__pycache__/graph_utils.*.pyc
%{python3_sitearch}/%{name}/kcc/__pycache__/kcc_utils.*.pyc
%{python3_sitearch}/%{name}/kcc/__pycache__/ldif_import_export.*.pyc

%dir %{python3_sitearch}/samba/provision
%{python3_sitearch}/%{name}/provision/backend.py
%{python3_sitearch}/%{name}/provision/common.py
%{python3_sitearch}/%{name}/provision/kerberos.py
%{python3_sitearch}/%{name}/provision/kerberos_implementation.py
%{python3_sitearch}/%{name}/provision/sambadns.py

%dir %{python3_sitearch}/samba/provision/__pycache__
%{python3_sitearch}/%{name}/provision/__init__.py
%{python3_sitearch}/%{name}/provision/__pycache__/__init__.*.pyc
%{python3_sitearch}/%{name}/provision/__pycache__/backend.*.pyc
%{python3_sitearch}/%{name}/provision/__pycache__/common.*.pyc
%{python3_sitearch}/%{name}/provision/__pycache__/kerberos.*.pyc
%{python3_sitearch}/%{name}/provision/__pycache__/kerberos_implementation.*.pyc
%{python3_sitearch}/%{name}/provision/__pycache__/sambadns.*.pyc

%{python3_sitearch}/%{name}/remove_dc.py
%endif

%files -n python3-%{name}-test
%dir %{python3_sitearch}/samba/tests
%{python3_sitearch}/samba/tests/__init__.py
%dir %{python3_sitearch}/samba/tests/__pycache__
%{python3_sitearch}/%{name}/tests/__pycache__/__init__.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/audit_log_base.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/audit_log_dsdb.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/audit_log_pass_change.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/auth.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/auth_log.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/auth_log_base.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/auth_log_pass_change.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/auth_log_ncalrpc.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/auth_log_netlogon.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/auth_log_netlogon_bad_creds.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/auth_log_samlogon.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/common.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/core.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/credentials.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/dckeytab.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/dns.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/dns_base.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/dns_forwarder.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/dns_invalid.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/dns_tkey.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/dns_wildcard.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/dsdb.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/dsdb_lock.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/dsdb_schema_attributes.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/docs.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/domain_backup.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/encrypted_secrets.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/gensec.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/get_opt.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/getdcname.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/glue.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/gpo.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/graph.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/group_audit.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/hostconfig.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/join.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/krb5_credentials.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/libsmb_samba_internal.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/loadparm.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/lsa_string.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/messaging.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/netbios.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/netcmd.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/net_join_no_spnego.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/net_join.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/netlogonsvc.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/ntacls.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/ntacls_backup.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/ntlmdisabled.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/pam_winbind.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/pam_winbind_warn_pwd_expire.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/param.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/password_hash.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/password_hash_fl2003.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/password_hash_fl2008.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/password_hash_gpgme.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/password_hash_ldap.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/password_quality.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/password_test.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/policy.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/posixacl.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/provision.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/pso.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/py_credentials.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/registry.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/s3idmapdb.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/s3param.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/s3passdb.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/s3registry.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/s3windb.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/samba3sam.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/samdb.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/samdb_api.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/security.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/smb.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/source.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/strings.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/subunitrun.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/tdb_util.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/unicodenames.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/upgrade.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/upgradeprovision.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/upgradeprovisionneeddc.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/xattr.*.pyc
%{python3_sitearch}/%{name}/tests/__pycache__/smbd_base.*.pyc
%{python3_sitearch}/%{name}/tests/audit_log_base.py
%{python3_sitearch}/%{name}/tests/audit_log_dsdb.py
%{python3_sitearch}/%{name}/tests/audit_log_pass_change.py
%{python3_sitearch}/%{name}/tests/auth.py
%{python3_sitearch}/%{name}/tests/auth_log.py
%{python3_sitearch}/%{name}/tests/auth_log_base.py
%{python3_sitearch}/%{name}/tests/auth_log_ncalrpc.py
%{python3_sitearch}/%{name}/tests/auth_log_netlogon_bad_creds.py
%{python3_sitearch}/%{name}/tests/auth_log_netlogon.py
%{python3_sitearch}/%{name}/tests/auth_log_pass_change.py
%{python3_sitearch}/%{name}/tests/auth_log_samlogon.py
%dir %{python3_sitearch}/samba/tests/blackbox
%{python3_sitearch}/samba/tests/blackbox/__init__.py
%dir %{python3_sitearch}/samba/tests/blackbox/__pycache__
%{python3_sitearch}/%{name}/tests/blackbox/__pycache__/__init__.*.pyc
%{python3_sitearch}/%{name}/tests/blackbox/__pycache__/check_output.*.pyc
%{python3_sitearch}/%{name}/tests/blackbox/__pycache__/ndrdump.*.pyc
%{python3_sitearch}/%{name}/tests/blackbox/__pycache__/samba_dnsupdate.*.pyc
%{python3_sitearch}/%{name}/tests/blackbox/__pycache__/smbcontrol.*.pyc
%{python3_sitearch}/%{name}/tests/blackbox/__pycache__/traffic_learner.*.pyc
%{python3_sitearch}/%{name}/tests/blackbox/__pycache__/traffic_replay.*.pyc
%{python3_sitearch}/%{name}/tests/blackbox/__pycache__/traffic_summary.*.pyc
%{python3_sitearch}/%{name}/tests/blackbox/check_output.py
%{python3_sitearch}/%{name}/tests/blackbox/ndrdump.py
%{python3_sitearch}/%{name}/tests/blackbox/samba_dnsupdate.py
%{python3_sitearch}/%{name}/tests/blackbox/smbcontrol.py
%{python3_sitearch}/%{name}/tests/blackbox/traffic_learner.py
%{python3_sitearch}/%{name}/tests/blackbox/traffic_replay.py
%{python3_sitearch}/%{name}/tests/blackbox/traffic_summary.py
%{python3_sitearch}/%{name}/tests/common.py
%{python3_sitearch}/%{name}/tests/core.py
%{python3_sitearch}/%{name}/tests/credentials.py
%dir %{python3_sitearch}/samba/tests/dcerpc
%{python3_sitearch}/samba/tests/dcerpc/__init__.py
%dir %{python3_sitearch}/samba/tests/dcerpc/__pycache__
%{python3_sitearch}/%{name}/tests/dcerpc/__pycache__/__init__.*.pyc
%{python3_sitearch}/%{name}/tests/dcerpc/__pycache__/array.*.pyc
%{python3_sitearch}/%{name}/tests/dcerpc/__pycache__/bare.*.pyc
%{python3_sitearch}/%{name}/tests/dcerpc/__pycache__/dnsserver.*.pyc
%{python3_sitearch}/%{name}/tests/dcerpc/__pycache__/misc.*.pyc
%{python3_sitearch}/%{name}/tests/dcerpc/__pycache__/raw_protocol.*.pyc
%{python3_sitearch}/%{name}/tests/dcerpc/__pycache__/raw_testcase.*.pyc
%{python3_sitearch}/%{name}/tests/dcerpc/__pycache__/registry.*.pyc
%{python3_sitearch}/%{name}/tests/dcerpc/__pycache__/rpc_talloc.*.pyc
%{python3_sitearch}/%{name}/tests/dcerpc/__pycache__/rpcecho.*.pyc
%{python3_sitearch}/%{name}/tests/dcerpc/__pycache__/sam.*.pyc
%{python3_sitearch}/%{name}/tests/dcerpc/__pycache__/srvsvc.*.pyc
%{python3_sitearch}/%{name}/tests/dcerpc/__pycache__/string.*.pyc
%{python3_sitearch}/%{name}/tests/dcerpc/__pycache__/testrpc.*.pyc
%{python3_sitearch}/%{name}/tests/dcerpc/array.py
%{python3_sitearch}/%{name}/tests/dcerpc/bare.py
%{python3_sitearch}/%{name}/tests/dcerpc/dnsserver.py
%{python3_sitearch}/%{name}/tests/dcerpc/misc.py
%{python3_sitearch}/%{name}/tests/dcerpc/raw_protocol.py
%{python3_sitearch}/%{name}/tests/dcerpc/raw_testcase.py
%{python3_sitearch}/%{name}/tests/dcerpc/registry.py
%{python3_sitearch}/%{name}/tests/dcerpc/rpc_talloc.py
%{python3_sitearch}/%{name}/tests/dcerpc/rpcecho.py
%{python3_sitearch}/%{name}/tests/dcerpc/sam.py
%{python3_sitearch}/%{name}/tests/dcerpc/srvsvc.py
%{python3_sitearch}/%{name}/tests/dcerpc/string.py
%{python3_sitearch}/%{name}/tests/dcerpc/testrpc.py
%{python3_sitearch}/%{name}/tests/dckeytab.py
%{python3_sitearch}/%{name}/tests/dns.py
%{python3_sitearch}/%{name}/tests/dns_base.py
%{python3_sitearch}/%{name}/tests/dns_forwarder.py
%dir %{python3_sitearch}/samba/tests/dns_forwarder_helpers
%{python3_sitearch}/%{name}/tests/dns_forwarder_helpers/__pycache__/server.*.pyc
%{python3_sitearch}/%{name}/tests/dns_forwarder_helpers/server.py
%{python3_sitearch}/%{name}/tests/dns_invalid.py
%{python3_sitearch}/%{name}/tests/dns_tkey.py
%{python3_sitearch}/%{name}/tests/dns_wildcard.py
%{python3_sitearch}/%{name}/tests/dsdb.py
%{python3_sitearch}/%{name}/tests/dsdb_lock.py
%{python3_sitearch}/%{name}/tests/dsdb_schema_attributes.py
%{python3_sitearch}/%{name}/tests/docs.py
%{python3_sitearch}/%{name}/tests/domain_backup.py
%dir %{python3_sitearch}/samba/tests/emulate
%{python3_sitearch}/samba/tests/emulate/__init__.py
%dir %{python3_sitearch}/samba/tests/emulate/__pycache__
%{python3_sitearch}/%{name}/tests/emulate/__pycache__/__init__.*.pyc
%{python3_sitearch}/%{name}/tests/emulate/__pycache__/traffic.*.pyc
%{python3_sitearch}/%{name}/tests/emulate/__pycache__/traffic_packet.*.pyc
%{python3_sitearch}/%{name}/tests/emulate/traffic.py
%{python3_sitearch}/%{name}/tests/emulate/traffic_packet.py
%{python3_sitearch}/%{name}/tests/encrypted_secrets.py
%{python3_sitearch}/%{name}/tests/gensec.py
%{python3_sitearch}/%{name}/tests/getdcname.py
%{python3_sitearch}/%{name}/tests/get_opt.py
%{python3_sitearch}/%{name}/tests/glue.py
%{python3_sitearch}/%{name}/tests/gpo.py
%{python3_sitearch}/%{name}/tests/graph.py
%{python3_sitearch}/%{name}/tests/group_audit.py
%{python3_sitearch}/%{name}/tests/hostconfig.py
%{python3_sitearch}/%{name}/tests/join.py
%dir %{python3_sitearch}/samba/tests/kcc
%{python3_sitearch}/samba/tests/kcc/__init__.py
%dir %{python3_sitearch}/samba/tests/kcc/__pycache__
%{python3_sitearch}/%{name}/tests/kcc/__pycache__/__init__.*.pyc
%{python3_sitearch}/%{name}/tests/kcc/__pycache__/graph.*.pyc
%{python3_sitearch}/%{name}/tests/kcc/__pycache__/graph_utils.*.pyc
%{python3_sitearch}/%{name}/tests/kcc/__pycache__/kcc_utils.*.pyc
%{python3_sitearch}/%{name}/tests/kcc/__pycache__/ldif_import_export.*.pyc
%{python3_sitearch}/%{name}/tests/kcc/graph.py
%{python3_sitearch}/%{name}/tests/kcc/graph_utils.py
%{python3_sitearch}/%{name}/tests/kcc/kcc_utils.py
%{python3_sitearch}/%{name}/tests/kcc/ldif_import_export.py
%{python3_sitearch}/%{name}/tests/krb5_credentials.py
%{python3_sitearch}/%{name}/tests/libsmb_samba_internal.py
%{python3_sitearch}/%{name}/tests/loadparm.py
%{python3_sitearch}/%{name}/tests/lsa_string.py
%{python3_sitearch}/%{name}/tests/messaging.py
%{python3_sitearch}/%{name}/tests/netbios.py
%{python3_sitearch}/%{name}/tests/netcmd.py
%{python3_sitearch}/%{name}/tests/net_join_no_spnego.py
%{python3_sitearch}/%{name}/tests/net_join.py
%{python3_sitearch}/%{name}/tests/netlogonsvc.py
%{python3_sitearch}/%{name}/tests/ntacls.py
%{python3_sitearch}/%{name}/tests/ntacls_backup.py
%{python3_sitearch}/%{name}/tests/ntlmdisabled.py
%{python3_sitearch}/%{name}/tests/pam_winbind.py
%{python3_sitearch}/%{name}/tests/pam_winbind_warn_pwd_expire.py
%{python3_sitearch}/%{name}/tests/param.py
%{python3_sitearch}/%{name}/tests/password_hash.py
%{python3_sitearch}/%{name}/tests/password_hash_fl2003.py
%{python3_sitearch}/%{name}/tests/password_hash_fl2008.py
%{python3_sitearch}/%{name}/tests/password_hash_gpgme.py
%{python3_sitearch}/%{name}/tests/password_hash_ldap.py
%{python3_sitearch}/%{name}/tests/password_quality.py
%{python3_sitearch}/%{name}/tests/password_test.py
%{python3_sitearch}/%{name}/tests/policy.py
%{python3_sitearch}/%{name}/tests/posixacl.py
%{python3_sitearch}/%{name}/tests/provision.py
%{python3_sitearch}/%{name}/tests/pso.py
%{python3_sitearch}/%{name}/tests/py_credentials.py
%{python3_sitearch}/%{name}/tests/registry.py
%{python3_sitearch}/%{name}/tests/s3idmapdb.py
%{python3_sitearch}/%{name}/tests/s3param.py
%{python3_sitearch}/%{name}/tests/s3passdb.py
%{python3_sitearch}/%{name}/tests/s3registry.py
%{python3_sitearch}/%{name}/tests/s3windb.py
%{python3_sitearch}/%{name}/tests/samba3sam.py
%dir %{python3_sitearch}/samba/tests/samba_tool
%{python3_sitearch}/samba/tests/samba_tool/__init__.py
%dir %{python3_sitearch}/samba/tests/samba_tool/__pycache__
%{python3_sitearch}/%{name}/tests/samba_tool/__pycache__/__init__.*.pyc
%{python3_sitearch}/%{name}/tests/samba_tool/__pycache__/base.*.pyc
%{python3_sitearch}/%{name}/tests/samba_tool/__pycache__/computer.*.pyc
%{python3_sitearch}/%{name}/tests/samba_tool/__pycache__/demote.*.pyc
%{python3_sitearch}/%{name}/tests/samba_tool/__pycache__/dnscmd.*.pyc
%{python3_sitearch}/%{name}/tests/samba_tool/__pycache__/forest.*.pyc
%{python3_sitearch}/%{name}/tests/samba_tool/__pycache__/fsmo.*.pyc
%{python3_sitearch}/%{name}/tests/samba_tool/__pycache__/gpo.*.pyc
%{python3_sitearch}/%{name}/tests/samba_tool/__pycache__/group.*.pyc
%{python3_sitearch}/%{name}/tests/samba_tool/__pycache__/help.*.pyc
%{python3_sitearch}/%{name}/tests/samba_tool/__pycache__/join.*.pyc
%{python3_sitearch}/%{name}/tests/samba_tool/__pycache__/ntacl.*.pyc
%{python3_sitearch}/%{name}/tests/samba_tool/__pycache__/ou.*.pyc
%{python3_sitearch}/%{name}/tests/samba_tool/__pycache__/passwordsettings.*.pyc
%{python3_sitearch}/%{name}/tests/samba_tool/__pycache__/processes.*.pyc
%{python3_sitearch}/%{name}/tests/samba_tool/__pycache__/provision_password_check.*.pyc
%{python3_sitearch}/%{name}/tests/samba_tool/__pycache__/rodc.*.pyc
%{python3_sitearch}/%{name}/tests/samba_tool/__pycache__/schema.*.pyc
%{python3_sitearch}/%{name}/tests/samba_tool/__pycache__/sites.*.pyc
%{python3_sitearch}/%{name}/tests/samba_tool/__pycache__/timecmd.*.pyc
%{python3_sitearch}/%{name}/tests/samba_tool/__pycache__/user.*.pyc
%{python3_sitearch}/%{name}/tests/samba_tool/__pycache__/user_check_password_script.*.pyc
%{python3_sitearch}/%{name}/tests/samba_tool/__pycache__/user_virtualCryptSHA.*.pyc
%{python3_sitearch}/%{name}/tests/samba_tool/__pycache__/user_wdigest.*.pyc
%{python3_sitearch}/%{name}/tests/samba_tool/__pycache__/visualize.*.pyc
%{python3_sitearch}/%{name}/tests/samba_tool/__pycache__/visualize_drs.*.pyc
%{python3_sitearch}/%{name}/tests/samba_tool/base.py
%{python3_sitearch}/%{name}/tests/samba_tool/computer.py
%{python3_sitearch}/%{name}/tests/samba_tool/demote.py
%{python3_sitearch}/%{name}/tests/samba_tool/dnscmd.py
%{python3_sitearch}/%{name}/tests/samba_tool/forest.py
%{python3_sitearch}/%{name}/tests/samba_tool/fsmo.py
%{python3_sitearch}/%{name}/tests/samba_tool/gpo.py
%{python3_sitearch}/%{name}/tests/samba_tool/group.py
%{python3_sitearch}/%{name}/tests/samba_tool/help.py
%{python3_sitearch}/%{name}/tests/samba_tool/join.py
%{python3_sitearch}/%{name}/tests/samba_tool/ntacl.py
%{python3_sitearch}/%{name}/tests/samba_tool/ou.py
%{python3_sitearch}/%{name}/tests/samba_tool/passwordsettings.py
%{python3_sitearch}/%{name}/tests/samba_tool/processes.py
%{python3_sitearch}/%{name}/tests/samba_tool/provision_password_check.py
%{python3_sitearch}/%{name}/tests/samba_tool/rodc.py
%{python3_sitearch}/%{name}/tests/samba_tool/schema.py
%{python3_sitearch}/%{name}/tests/samba_tool/sites.py
%{python3_sitearch}/%{name}/tests/samba_tool/timecmd.py
%{python3_sitearch}/%{name}/tests/samba_tool/user.py
%{python3_sitearch}/%{name}/tests/samba_tool/user_check_password_script.py
%{python3_sitearch}/%{name}/tests/samba_tool/user_virtualCryptSHA.py
%{python3_sitearch}/%{name}/tests/samba_tool/user_wdigest.py
%{python3_sitearch}/%{name}/tests/samba_tool/visualize.py
%{python3_sitearch}/%{name}/tests/samba_tool/visualize_drs.py
%{python3_sitearch}/%{name}/tests/samdb.py
%{python3_sitearch}/%{name}/tests/samdb_api.py
%{python3_sitearch}/%{name}/tests/security.py
%{python3_sitearch}/%{name}/tests/smb.py
%{python3_sitearch}/%{name}/tests/source.py
%{python3_sitearch}/%{name}/tests/strings.py
%{python3_sitearch}/%{name}/tests/subunitrun.py
%{python3_sitearch}/%{name}/tests/tdb_util.py
%{python3_sitearch}/%{name}/tests/unicodenames.py
%{python3_sitearch}/%{name}/tests/upgrade.py
%{python3_sitearch}/%{name}/tests/upgradeprovision.py
%{python3_sitearch}/%{name}/tests/upgradeprovisionneeddc.py
%{python3_sitearch}/%{name}/tests/xattr.py
%{python3_sitearch}/%{name}/tests/smbd_base.py
%dir %{python3_sitearch}/samba/web_server
%{python3_sitearch}/samba/web_server/__init__.py
%dir %{python3_sitearch}/samba/web_server/__pycache__
%{python3_sitearch}/%{name}/web_server/__pycache__/__init__.*.pyc
%{python3_sitearch}/%{name}/werror.*.so
%{python3_sitearch}/%{name}/xattr.py
%{python3_sitearch}/%{name}/xattr_native.*.so
%{python3_sitearch}/%{name}/xattr_tdb.*.so

%files test
%{_bindir}/gentest
%{_bindir}/locktest
%{_bindir}/masktest
%{_bindir}/ndrdump
%{_bindir}/smbtorture

%if %{with testsuite}
%{_libdir}/%{name}/libnss-wrapper.so
%{_libdir}/%{name}/libsocket-wrapper.so
%{_libdir}/%{name}/libuid-wrapper.so
%endif
%if %with_dc
%{_libdir}/%{name}/libdlz-bind9-for-torture-samba4.so
%else
%{_libdir}/%{name}/libdsdb-module-samba4.so
%endif

%files winbind
%{_libdir}/%{name}/idmap
%{_libdir}/%{name}/nss_info
%{_libdir}/%{name}/libnss-info-samba4.so
%{_libdir}/%{name}/libidmap-samba4.so
%{_sbindir}/winbindd
%attr(750,root,wbpriv) %dir /var/lib/samba/winbindd_privileged
%{_unitdir}/winbind.service
%{_sysconfdir}/NetworkManager/dispatcher.d/30-winbind

%files winbind-clients
%{_bindir}/ntlm_auth
%{_bindir}/wbinfo
%{_libdir}/samba/krb5/winbind_krb5_localauth.so

%files winbind-krb5-locator
%ghost %{_libdir}/krb5/plugins/libkrb5/winbind_krb5_locator.so
%{_libdir}/samba/krb5/winbind_krb5_locator.so

%files winbind-modules
%{_libdir}/libnss_winbind.so*
%{_libdir}/libnss_wins.so*
%{_libdir}/security/pam_winbind.so
%config(noreplace) %{_sysconfdir}/security/pam_winbind.conf

%if %with_clustering_support
%files -n ctdb
%doc ctdb/README
%doc ctdb/doc/examples
%config(noreplace, missingok) %{_sysconfdir}/sysconfig/ctdb
%dir %{_sysconfdir}/ctdb
%config(noreplace) %{_sysconfdir}/ctdb/*.sh
%config(noreplace) %{_sysconfdir}/ctdb/ctdb.conf

%{_sysconfdir}/ctdb/functions
%{_sysconfdir}/ctdb/statd-callout
%{_sysconfdir}/ctdb/nfs-linux-kernel-callout
%config %{_sysconfdir}/sudoers.d/ctdb

%dir %{_sysconfdir}/ctdb/events
%dir %{_sysconfdir}/ctdb/events/notification
%{_sysconfdir}/ctdb/events/notification/README

%dir %{_sysconfdir}/ctdb/nfs-checks.d
%{_sysconfdir}/ctdb/nfs-checks.d/README
%config(noreplace) %{_sysconfdir}/ctdb/nfs-checks.d/*.check

%{_bindir}/ctdb
%{_bindir}/ctdb_diagnostics
%{_bindir}/ltdbtool
%{_bindir}/onnode
%{_bindir}/ping_pong
%{_sbindir}/ctdbd
%{_sbindir}/ctdbd_wrapper

%dir %{_libexecdir}/ctdb
%{_libexecdir}/ctdb/ctdb*
%{_libexecdir}/ctdb/smnotify

%dir %{_localstatedir}/lib/ctdb/
%{_tmpfilesdir}/ctdb.conf
%{_unitdir}/ctdb.service

%dir %{_datadir}/ctdb
%dir %{_datadir}/ctdb/events
%dir %{_datadir}/ctdb/events/legacy/
%{_datadir}/ctdb/events/legacy/00.ctdb.script
%{_datadir}/ctdb/events/legacy/01.reclock.script
%{_datadir}/ctdb/events/legacy/05.system.script
%{_datadir}/ctdb/events/legacy/06.nfs.script
%{_datadir}/ctdb/events/legacy/10.interface.script
%{_datadir}/ctdb/events/legacy/11.natgw.script
%{_datadir}/ctdb/events/legacy/11.routing.script
%{_datadir}/ctdb/events/legacy/13.per_ip_routing.script
%{_datadir}/ctdb/events/legacy/20.multipathd.script
%{_datadir}/ctdb/events/legacy/31.clamd.script
%{_datadir}/ctdb/events/legacy/40.vsftpd.script
%{_datadir}/ctdb/events/legacy/41.httpd.script
%{_datadir}/ctdb/events/legacy/49.winbind.script
%{_datadir}/ctdb/events/legacy/50.samba.script
%{_datadir}/ctdb/events/legacy/60.nfs.script
%{_datadir}/ctdb/events/legacy/70.iscsi.script
%{_datadir}/ctdb/events/legacy/91.lvs.script

%files -n ctdb-tests
%doc ctdb/tests/README
%{_bindir}/ctdb_run_tests
%{_bindir}/ctdb_run_cluster_tests

%dir %{_libexecdir}/ctdb
%dir %{_libexecdir}/ctdb/tests
%{_libexecdir}/ctdb/tests/*

%dir %{_datadir}/ctdb/tests
%dir %{_datadir}/ctdb/tests/complex
%{_datadir}/ctdb/tests/complex/*
%exclude %{_datadir}/ctdb/tests/complex/scripts

%dir %{_datadir}/ctdb/tests/complex/scripts
%{_datadir}/ctdb/tests/complex/scripts/local.bash

%dir %{_datadir}/ctdb/tests/cunit
%{_datadir}/ctdb/tests/cunit/*

%dir %{_datadir}/ctdb/tests/eventd
%{_datadir}/ctdb/tests/eventd/README
%dir %{_datadir}/ctdb/tests/eventd/etc-ctdb
%{_datadir}/ctdb/tests/eventd/etc-ctdb/ctdb.conf
%{_datadir}/ctdb/tests/eventd/etc-ctdb/debug-script.sh
%dir %{_datadir}/ctdb/tests/eventd/etc-ctdb/events
%dir %{_datadir}/ctdb/tests/eventd/etc-ctdb/events/data
%{_datadir}/ctdb/tests/eventd/etc-ctdb/events/data/README
%{_datadir}/ctdb/tests/eventd/etc-ctdb/events/data/03.notalink.script
%dir %{_datadir}/ctdb/tests/eventd/etc-ctdb/events/empty
%{_datadir}/ctdb/tests/eventd/etc-ctdb/events/empty/README
%dir %{_datadir}/ctdb/tests/eventd/etc-ctdb/events/multi
%{_datadir}/ctdb/tests/eventd/etc-ctdb/events/multi/01.test.script
%{_datadir}/ctdb/tests/eventd/etc-ctdb/events/multi/02.test.script
%{_datadir}/ctdb/tests/eventd/etc-ctdb/events/multi/03.test.script
%dir %{_datadir}/ctdb/tests/eventd/etc-ctdb/events/random
%{_datadir}/ctdb/tests/eventd/etc-ctdb/events/random/01.disabled.script
%{_datadir}/ctdb/tests/eventd/etc-ctdb/events/random/02.enabled.script
%{_datadir}/ctdb/tests/eventd/etc-ctdb/events/random/README.script
%{_datadir}/ctdb/tests/eventd/etc-ctdb/events/random/a.script
%dir %{_datadir}/ctdb/tests/eventd/etc-ctdb/share
%dir %{_datadir}/ctdb/tests/eventd/etc-ctdb/share/events/
%dir %{_datadir}/ctdb/tests/eventd/etc-ctdb/share/events/data
%{_datadir}/ctdb/tests/eventd/etc-ctdb/share/events/data/01.dummy.script
%{_datadir}/ctdb/tests/eventd/etc-ctdb/share/events/data/02.disabled.script
%dir %{_datadir}/ctdb/tests/eventd/etc-ctdb/share/events/empty
%{_datadir}/ctdb/tests/eventd/etc-ctdb/share/events/empty/README
%dir %{_datadir}/ctdb/tests/eventd/etc-ctdb/share/events/random
%{_datadir}/ctdb/tests/eventd/etc-ctdb/share/events/random/01.disabled.script
%{_datadir}/ctdb/tests/eventd/etc-ctdb/share/events/random/02.enabled.script
%{_datadir}/ctdb/tests/eventd/etc-ctdb/share/events/random/a.script
%{_datadir}/ctdb/tests/eventd/etc-ctdb/share/events/random/README.script
%{_datadir}/ctdb/tests/eventd/eventd_001.sh
%{_datadir}/ctdb/tests/eventd/eventd_002.sh
%{_datadir}/ctdb/tests/eventd/eventd_003.sh
%{_datadir}/ctdb/tests/eventd/eventd_004.sh
%{_datadir}/ctdb/tests/eventd/eventd_005.sh
%{_datadir}/ctdb/tests/eventd/eventd_006.sh
%{_datadir}/ctdb/tests/eventd/eventd_007.sh
%{_datadir}/ctdb/tests/eventd/eventd_008.sh
%{_datadir}/ctdb/tests/eventd/eventd_009.sh
%{_datadir}/ctdb/tests/eventd/eventd_011.sh
%{_datadir}/ctdb/tests/eventd/eventd_012.sh
%{_datadir}/ctdb/tests/eventd/eventd_013.sh
%{_datadir}/ctdb/tests/eventd/eventd_014.sh
%{_datadir}/ctdb/tests/eventd/eventd_021.sh
%{_datadir}/ctdb/tests/eventd/eventd_022.sh
%{_datadir}/ctdb/tests/eventd/eventd_023.sh
%{_datadir}/ctdb/tests/eventd/eventd_024.sh
%{_datadir}/ctdb/tests/eventd/eventd_031.sh
%{_datadir}/ctdb/tests/eventd/eventd_032.sh
%{_datadir}/ctdb/tests/eventd/eventd_033.sh
%{_datadir}/ctdb/tests/eventd/eventd_041.sh
%{_datadir}/ctdb/tests/eventd/eventd_042.sh
%{_datadir}/ctdb/tests/eventd/eventd_043.sh
%{_datadir}/ctdb/tests/eventd/eventd_044.sh
%{_datadir}/ctdb/tests/eventd/eventd_051.sh
%{_datadir}/ctdb/tests/eventd/eventd_052.sh
%dir %{_datadir}/ctdb/tests/eventd/scripts
%{_datadir}/ctdb/tests/eventd/scripts/local.sh

%dir %{_datadir}/ctdb/tests/eventscripts
%{_datadir}/ctdb/tests/eventscripts/README
%{_datadir}/ctdb/tests/eventscripts/00.ctdb.init.001.sh
%{_datadir}/ctdb/tests/eventscripts/00.ctdb.init.002.sh
%{_datadir}/ctdb/tests/eventscripts/00.ctdb.init.003.sh
%{_datadir}/ctdb/tests/eventscripts/00.ctdb.init.004.sh
%{_datadir}/ctdb/tests/eventscripts/00.ctdb.init.005.sh
%{_datadir}/ctdb/tests/eventscripts/00.ctdb.init.006.sh
%{_datadir}/ctdb/tests/eventscripts/00.ctdb.init.007.sh
%{_datadir}/ctdb/tests/eventscripts/00.ctdb.init.008.sh
%{_datadir}/ctdb/tests/eventscripts/00.ctdb.init.009.sh
%{_datadir}/ctdb/tests/eventscripts/00.ctdb.setup.001.sh
%{_datadir}/ctdb/tests/eventscripts/00.ctdb.setup.002.sh
%{_datadir}/ctdb/tests/eventscripts/00.ctdb.setup.003.sh
%{_datadir}/ctdb/tests/eventscripts/00.ctdb.setup.004.sh
%{_datadir}/ctdb/tests/eventscripts/01.reclock.monitor.001.sh
%{_datadir}/ctdb/tests/eventscripts/01.reclock.monitor.002.sh
%{_datadir}/ctdb/tests/eventscripts/01.reclock.monitor.003.sh
%{_datadir}/ctdb/tests/eventscripts/01.reclock.monitor.004.sh
%{_datadir}/ctdb/tests/eventscripts/01.reclock.monitor.005.sh
%{_datadir}/ctdb/tests/eventscripts/05.system.monitor.001.sh
%{_datadir}/ctdb/tests/eventscripts/05.system.monitor.002.sh
%{_datadir}/ctdb/tests/eventscripts/05.system.monitor.003.sh
%{_datadir}/ctdb/tests/eventscripts/05.system.monitor.004.sh
%{_datadir}/ctdb/tests/eventscripts/05.system.monitor.005.sh
%{_datadir}/ctdb/tests/eventscripts/05.system.monitor.006.sh
%{_datadir}/ctdb/tests/eventscripts/05.system.monitor.007.sh
%{_datadir}/ctdb/tests/eventscripts/05.system.monitor.011.sh
%{_datadir}/ctdb/tests/eventscripts/05.system.monitor.012.sh
%{_datadir}/ctdb/tests/eventscripts/05.system.monitor.013.sh
%{_datadir}/ctdb/tests/eventscripts/05.system.monitor.014.sh
%{_datadir}/ctdb/tests/eventscripts/05.system.monitor.015.sh
%{_datadir}/ctdb/tests/eventscripts/05.system.monitor.016.sh
%{_datadir}/ctdb/tests/eventscripts/05.system.monitor.017.sh
%{_datadir}/ctdb/tests/eventscripts/05.system.monitor.018.sh
%{_datadir}/ctdb/tests/eventscripts/06.nfs.releaseip.001.sh
%{_datadir}/ctdb/tests/eventscripts/06.nfs.releaseip.002.sh
%{_datadir}/ctdb/tests/eventscripts/06.nfs.takeip.001.sh
%{_datadir}/ctdb/tests/eventscripts/06.nfs.takeip.002.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.010.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.011.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.012.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.013.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.init.001.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.init.002.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.init.021.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.init.022.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.init.023.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.monitor.001.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.monitor.002.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.monitor.003.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.monitor.004.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.monitor.005.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.monitor.006.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.monitor.009.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.monitor.010.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.monitor.011.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.monitor.012.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.monitor.013.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.monitor.014.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.monitor.015.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.monitor.016.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.monitor.017.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.monitor.018.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.multi.001.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.releaseip.001.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.releaseip.002.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.startup.001.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.startup.002.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.takeip.001.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.takeip.002.sh
%{_datadir}/ctdb/tests/eventscripts/10.interface.takeip.003.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.001.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.002.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.003.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.004.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.011.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.012.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.013.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.014.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.015.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.021.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.022.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.023.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.024.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.025.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.031.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.041.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.042.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.051.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.052.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.053.sh
%{_datadir}/ctdb/tests/eventscripts/11.natgw.054.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.001.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.002.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.003.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.004.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.005.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.006.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.007.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.008.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.009.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.010.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.011.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.012.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.013.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.014.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.015.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.016.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.017.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.018.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.019.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.021.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.022.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.023.sh
%{_datadir}/ctdb/tests/eventscripts/13.per_ip_routing.024.sh
%{_datadir}/ctdb/tests/eventscripts/20.multipathd.monitor.001.sh
%{_datadir}/ctdb/tests/eventscripts/20.multipathd.monitor.002.sh
%{_datadir}/ctdb/tests/eventscripts/20.multipathd.monitor.003.sh
%{_datadir}/ctdb/tests/eventscripts/20.multipathd.monitor.004.sh
%{_datadir}/ctdb/tests/eventscripts/31.clamd.monitor.002.sh
%{_datadir}/ctdb/tests/eventscripts/31.clamd.monitor.003.sh
%{_datadir}/ctdb/tests/eventscripts/40.vsftpd.monitor.002.sh
%{_datadir}/ctdb/tests/eventscripts/40.vsftpd.shutdown.002.sh
%{_datadir}/ctdb/tests/eventscripts/40.vsftpd.startup.002.sh
%{_datadir}/ctdb/tests/eventscripts/41.httpd.monitor.002.sh
%{_datadir}/ctdb/tests/eventscripts/41.httpd.shutdown.002.sh
%{_datadir}/ctdb/tests/eventscripts/41.httpd.startup.002.sh
%{_datadir}/ctdb/tests/eventscripts/49.winbind.monitor.101.sh
%{_datadir}/ctdb/tests/eventscripts/49.winbind.monitor.102.sh
%{_datadir}/ctdb/tests/eventscripts/49.winbind.shutdown.002.sh
%{_datadir}/ctdb/tests/eventscripts/49.winbind.startup.002.sh
%{_datadir}/ctdb/tests/eventscripts/50.samba.monitor.101.sh
%{_datadir}/ctdb/tests/eventscripts/50.samba.monitor.103.sh
%{_datadir}/ctdb/tests/eventscripts/50.samba.monitor.104.sh
%{_datadir}/ctdb/tests/eventscripts/50.samba.monitor.105.sh
%{_datadir}/ctdb/tests/eventscripts/50.samba.monitor.106.sh
%{_datadir}/ctdb/tests/eventscripts/50.samba.monitor.110.sh
%{_datadir}/ctdb/tests/eventscripts/50.samba.monitor.111.sh
%{_datadir}/ctdb/tests/eventscripts/50.samba.monitor.112.sh
%{_datadir}/ctdb/tests/eventscripts/50.samba.monitor.113.sh
%{_datadir}/ctdb/tests/eventscripts/50.samba.shutdown.001.sh
%{_datadir}/ctdb/tests/eventscripts/50.samba.shutdown.002.sh
%{_datadir}/ctdb/tests/eventscripts/50.samba.shutdown.011.sh
%{_datadir}/ctdb/tests/eventscripts/50.samba.startup.011.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.101.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.102.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.103.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.104.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.105.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.106.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.107.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.108.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.109.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.111.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.112.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.113.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.114.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.121.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.122.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.131.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.132.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.141.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.142.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.143.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.144.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.151.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.152.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.153.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.161.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.monitor.162.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.multi.001.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.multi.002.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.releaseip.001.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.releaseip.002.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.shutdown.001.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.shutdown.002.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.startup.001.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.startup.002.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.takeip.001.sh
%{_datadir}/ctdb/tests/eventscripts/60.nfs.takeip.002.sh
%{_datadir}/ctdb/tests/eventscripts/91.lvs.001.sh
%{_datadir}/ctdb/tests/eventscripts/91.lvs.ipreallocated.011.sh
%{_datadir}/ctdb/tests/eventscripts/91.lvs.ipreallocated.012.sh
%{_datadir}/ctdb/tests/eventscripts/91.lvs.ipreallocated.013.sh
%{_datadir}/ctdb/tests/eventscripts/91.lvs.ipreallocated.014.sh
%{_datadir}/ctdb/tests/eventscripts/91.lvs.monitor.001.sh
%{_datadir}/ctdb/tests/eventscripts/91.lvs.monitor.002.sh
%{_datadir}/ctdb/tests/eventscripts/91.lvs.monitor.003.sh
%{_datadir}/ctdb/tests/eventscripts/91.lvs.shutdown.001.sh
%{_datadir}/ctdb/tests/eventscripts/91.lvs.shutdown.002.sh
%{_datadir}/ctdb/tests/eventscripts/91.lvs.startup.001.sh
%{_datadir}/ctdb/tests/eventscripts/91.lvs.startup.002.sh
%{_datadir}/ctdb/tests/eventscripts/statd-callout.001.sh
%{_datadir}/ctdb/tests/eventscripts/statd-callout.002.sh
%{_datadir}/ctdb/tests/eventscripts/statd-callout.003.sh
%{_datadir}/ctdb/tests/eventscripts/statd-callout.004.sh
%{_datadir}/ctdb/tests/eventscripts/statd-callout.005.sh
%{_datadir}/ctdb/tests/eventscripts/statd-callout.006.sh
%{_datadir}/ctdb/tests/eventscripts/statd-callout.007.sh

%dir %{_datadir}/ctdb/tests/eventscripts/etc-ctdb
%{_datadir}/ctdb/tests/eventscripts/etc-ctdb/public_addresses
%{_datadir}/ctdb/tests/eventscripts/etc-ctdb/rc.local

%dir %{_datadir}/ctdb/tests/eventscripts/etc
%dir %{_datadir}/ctdb/tests/eventscripts/etc/init.d
%{_datadir}/ctdb/tests/eventscripts/etc/init.d/nfs
%{_datadir}/ctdb/tests/eventscripts/etc/init.d/nfslock

%dir %{_datadir}/ctdb/tests/eventscripts/etc/samba
%{_datadir}/ctdb/tests/eventscripts/etc/samba/smb.conf

%dir %{_datadir}/ctdb/tests/eventscripts/etc/sysconfig
%{_datadir}/ctdb/tests/eventscripts/etc/sysconfig/nfs

%dir %{_datadir}/ctdb/tests/eventscripts/scripts
%{_datadir}/ctdb/tests/eventscripts/scripts/local.sh
%{_datadir}/ctdb/tests/eventscripts/scripts/00.ctdb.sh
%{_datadir}/ctdb/tests/eventscripts/scripts/01.reclock.sh
%{_datadir}/ctdb/tests/eventscripts/scripts/05.system.sh
%{_datadir}/ctdb/tests/eventscripts/scripts/06.nfs.sh
%{_datadir}/ctdb/tests/eventscripts/scripts/10.interface.sh
%{_datadir}/ctdb/tests/eventscripts/scripts/11.natgw.sh
%{_datadir}/ctdb/tests/eventscripts/scripts/13.per_ip_routing.sh
%{_datadir}/ctdb/tests/eventscripts/scripts/20.multipathd.sh
%{_datadir}/ctdb/tests/eventscripts/scripts/31.clamd.sh
%{_datadir}/ctdb/tests/eventscripts/scripts/40.vsftpd.sh
%{_datadir}/ctdb/tests/eventscripts/scripts/41.httpd.sh
%{_datadir}/ctdb/tests/eventscripts/scripts/49.winbind.sh
%{_datadir}/ctdb/tests/eventscripts/scripts/50.samba.sh
%{_datadir}/ctdb/tests/eventscripts/scripts/60.nfs.sh
%{_datadir}/ctdb/tests/eventscripts/scripts/91.lvs.sh
%{_datadir}/ctdb/tests/eventscripts/scripts/statd-callout.sh

%dir %{_datadir}/ctdb/tests/eventscripts/stubs
%{_datadir}/ctdb/tests/eventscripts/stubs/ctdb
%{_datadir}/ctdb/tests/eventscripts/stubs/ctdb-config
%{_datadir}/ctdb/tests/eventscripts/stubs/ctdb_killtcp
%{_datadir}/ctdb/tests/eventscripts/stubs/ctdb_lvs
%{_datadir}/ctdb/tests/eventscripts/stubs/ctdb_natgw
%{_datadir}/ctdb/tests/eventscripts/stubs/date
%{_datadir}/ctdb/tests/eventscripts/stubs/df
%{_datadir}/ctdb/tests/eventscripts/stubs/ethtool
%{_datadir}/ctdb/tests/eventscripts/stubs/exportfs
%{_datadir}/ctdb/tests/eventscripts/stubs/id
%{_datadir}/ctdb/tests/eventscripts/stubs/ip
%{_datadir}/ctdb/tests/eventscripts/stubs/ip6tables
%{_datadir}/ctdb/tests/eventscripts/stubs/iptables
%{_datadir}/ctdb/tests/eventscripts/stubs/ipvsadm
%{_datadir}/ctdb/tests/eventscripts/stubs/kill
%{_datadir}/ctdb/tests/eventscripts/stubs/killall
%{_datadir}/ctdb/tests/eventscripts/stubs/multipath
%{_datadir}/ctdb/tests/eventscripts/stubs/net
%{_datadir}/ctdb/tests/eventscripts/stubs/pidof
%{_datadir}/ctdb/tests/eventscripts/stubs/pkill
%{_datadir}/ctdb/tests/eventscripts/stubs/ps
%{_datadir}/ctdb/tests/eventscripts/stubs/rm
%{_datadir}/ctdb/tests/eventscripts/stubs/rpc.lockd
%{_datadir}/ctdb/tests/eventscripts/stubs/rpc.mountd
%{_datadir}/ctdb/tests/eventscripts/stubs/rpc.rquotad
%{_datadir}/ctdb/tests/eventscripts/stubs/rpc.statd
%{_datadir}/ctdb/tests/eventscripts/stubs/rpcinfo
%{_datadir}/ctdb/tests/eventscripts/stubs/service
%{_datadir}/ctdb/tests/eventscripts/stubs/sleep
%{_datadir}/ctdb/tests/eventscripts/stubs/smnotify
%{_datadir}/ctdb/tests/eventscripts/stubs/ss
%{_datadir}/ctdb/tests/eventscripts/stubs/tdbdump
%{_datadir}/ctdb/tests/eventscripts/stubs/tdbtool
%{_datadir}/ctdb/tests/eventscripts/stubs/testparm
%{_datadir}/ctdb/tests/eventscripts/stubs/timeout
%{_datadir}/ctdb/tests/eventscripts/stubs/wbinfo

%dir %{_datadir}/ctdb/tests/onnode
%{_datadir}/ctdb/tests/onnode/0001.sh
%{_datadir}/ctdb/tests/onnode/0002.sh
%{_datadir}/ctdb/tests/onnode/0003.sh
%{_datadir}/ctdb/tests/onnode/0004.sh
%{_datadir}/ctdb/tests/onnode/0005.sh
%{_datadir}/ctdb/tests/onnode/0006.sh
%{_datadir}/ctdb/tests/onnode/0070.sh
%{_datadir}/ctdb/tests/onnode/0071.sh
%{_datadir}/ctdb/tests/onnode/0072.sh
%{_datadir}/ctdb/tests/onnode/0075.sh

%dir %{_datadir}/ctdb/tests/onnode/etc-ctdb
%{_datadir}/ctdb/tests/onnode/etc-ctdb/nodes

%dir %{_datadir}/ctdb/tests/onnode/scripts
%{_datadir}/ctdb/tests/onnode/scripts/local.sh

%dir %{_datadir}/ctdb/tests/onnode/stubs
%{_datadir}/ctdb/tests/onnode/stubs/ctdb
%{_datadir}/ctdb/tests/onnode/stubs/ssh

%dir %{_datadir}/ctdb/tests/scripts
%{_datadir}/ctdb/tests/scripts/common.sh
%{_datadir}/ctdb/tests/scripts/integration.bash
%{_datadir}/ctdb/tests/scripts/script_install_paths.sh
%{_datadir}/ctdb/tests/scripts/test_wrap
%{_datadir}/ctdb/tests/scripts/unit.sh

%dir %{_datadir}/ctdb/tests/shellcheck
%{_datadir}/ctdb/tests/shellcheck/base_scripts.sh
%{_datadir}/ctdb/tests/shellcheck/ctdb_helpers.sh
%{_datadir}/ctdb/tests/shellcheck/ctdbd_wrapper.sh
%{_datadir}/ctdb/tests/shellcheck/event_scripts.sh
%{_datadir}/ctdb/tests/shellcheck/functions.sh
%{_datadir}/ctdb/tests/shellcheck/init_script.sh
%{_datadir}/ctdb/tests/shellcheck/tools.sh

%dir %{_datadir}/ctdb/tests/shellcheck/scripts
%{_datadir}/ctdb/tests/shellcheck/scripts/local.sh

%dir %{_datadir}/ctdb/tests/simple
%{_datadir}/ctdb/tests/simple/README
%{_datadir}/ctdb/tests/simple/00_ctdb_init.sh
%{_datadir}/ctdb/tests/simple/00_ctdb_onnode.sh
%{_datadir}/ctdb/tests/simple/01_ctdb_version.sh
%{_datadir}/ctdb/tests/simple/02_ctdb_listvars.sh
%{_datadir}/ctdb/tests/simple/03_ctdb_getvar.sh
%{_datadir}/ctdb/tests/simple/04_ctdb_setvar.sh
%{_datadir}/ctdb/tests/simple/05_ctdb_listnodes.sh
%{_datadir}/ctdb/tests/simple/06_ctdb_getpid.sh
%{_datadir}/ctdb/tests/simple/07_ctdb_process_exists.sh
%{_datadir}/ctdb/tests/simple/08_ctdb_isnotrecmaster.sh
%{_datadir}/ctdb/tests/simple/09_ctdb_ping.sh
%{_datadir}/ctdb/tests/simple/11_ctdb_ip.sh
%{_datadir}/ctdb/tests/simple/12_ctdb_getdebug.sh
%{_datadir}/ctdb/tests/simple/13_ctdb_setdebug.sh
%{_datadir}/ctdb/tests/simple/14_ctdb_statistics.sh
%{_datadir}/ctdb/tests/simple/15_ctdb_statisticsreset.sh
%{_datadir}/ctdb/tests/simple/16_ctdb_config_add_ip.sh
%{_datadir}/ctdb/tests/simple/17_ctdb_config_delete_ip.sh
%{_datadir}/ctdb/tests/simple/18_ctdb_reloadips.sh
%{_datadir}/ctdb/tests/simple/19_ip_takeover_noop.sh
%{_datadir}/ctdb/tests/simple/20_delip_iface_gc.sh
%{_datadir}/ctdb/tests/simple/21_ctdb_attach.sh
%{_datadir}/ctdb/tests/simple/23_ctdb_moveip.sh
%{_datadir}/ctdb/tests/simple/24_ctdb_getdbmap.sh
%{_datadir}/ctdb/tests/simple/25_dumpmemory.sh
%{_datadir}/ctdb/tests/simple/26_ctdb_config_check_error_on_unreachable_ctdb.sh
%{_datadir}/ctdb/tests/simple/27_ctdb_detach.sh
%{_datadir}/ctdb/tests/simple/28_zero_eventscripts.sh
%{_datadir}/ctdb/tests/simple/31_ctdb_disable.sh
%{_datadir}/ctdb/tests/simple/32_ctdb_enable.sh
%{_datadir}/ctdb/tests/simple/35_ctdb_getreclock.sh
%{_datadir}/ctdb/tests/simple/41_ctdb_stop.sh
%{_datadir}/ctdb/tests/simple/42_ctdb_continue.sh
%{_datadir}/ctdb/tests/simple/43_stop_recmaster_yield.sh
%{_datadir}/ctdb/tests/simple/51_message_ring.sh
%{_datadir}/ctdb/tests/simple/52_fetch_ring.sh
%{_datadir}/ctdb/tests/simple/53_transaction_loop.sh
%{_datadir}/ctdb/tests/simple/54_transaction_loop_recovery.sh
%{_datadir}/ctdb/tests/simple/55_ctdb_ptrans.sh
%{_datadir}/ctdb/tests/simple/56_replicated_transaction_recovery.sh
%{_datadir}/ctdb/tests/simple/58_ctdb_restoredb.sh
%{_datadir}/ctdb/tests/simple/60_recoverd_missing_ip.sh
%{_datadir}/ctdb/tests/simple/70_recoverpdbbyseqnum.sh
%{_datadir}/ctdb/tests/simple/71_ctdb_wipedb.sh
%{_datadir}/ctdb/tests/simple/72_update_record_persistent.sh
%{_datadir}/ctdb/tests/simple/73_tunable_NoIPTakeover.sh
%{_datadir}/ctdb/tests/simple/75_readonly_records_basic.sh
%{_datadir}/ctdb/tests/simple/76_ctdb_pdb_recovery.sh
%{_datadir}/ctdb/tests/simple/77_ctdb_db_recovery.sh
%{_datadir}/ctdb/tests/simple/78_ctdb_large_db_recovery.sh
%{_datadir}/ctdb/tests/simple/79_volatile_db_traverse.sh
%{_datadir}/ctdb/tests/simple/80_ctdb_traverse.sh
%{_datadir}/ctdb/tests/simple/81_tunnel_ring.sh
%{_datadir}/ctdb/tests/simple/90_debug_hung_script.sh
%{_datadir}/ctdb/tests/simple/99_daemons_shutdown.sh

%dir %{_datadir}/ctdb/tests/simple/etc-ctdb
%dir %{_datadir}/ctdb/tests/simple/etc-ctdb/events
%dir %{_datadir}/ctdb/tests/simple/etc-ctdb/events/legacy
%{_datadir}/ctdb/tests/simple/etc-ctdb/events/legacy/00.test.script

%dir %{_datadir}/ctdb/tests/simple/scripts
%{_datadir}/ctdb/tests/simple/scripts/local.bash
%{_datadir}/ctdb/tests/simple/scripts/local_daemons.bash
%{_datadir}/ctdb/tests/simple/scripts/ssh_local_daemons.sh

%dir %{_datadir}/ctdb/tests/takeover
%{_datadir}/ctdb/tests/takeover/README
%{_datadir}/ctdb/tests/takeover/det.001.sh
%{_datadir}/ctdb/tests/takeover/det.002.sh
%{_datadir}/ctdb/tests/takeover/det.003.sh
%{_datadir}/ctdb/tests/takeover/lcp2.001.sh
%{_datadir}/ctdb/tests/takeover/lcp2.002.sh
%{_datadir}/ctdb/tests/takeover/lcp2.003.sh
%{_datadir}/ctdb/tests/takeover/lcp2.004.sh
%{_datadir}/ctdb/tests/takeover/lcp2.005.sh
%{_datadir}/ctdb/tests/takeover/lcp2.006.sh
%{_datadir}/ctdb/tests/takeover/lcp2.007.sh
%{_datadir}/ctdb/tests/takeover/lcp2.008.sh
%{_datadir}/ctdb/tests/takeover/lcp2.009.sh
%{_datadir}/ctdb/tests/takeover/lcp2.010.sh
%{_datadir}/ctdb/tests/takeover/lcp2.011.sh
%{_datadir}/ctdb/tests/takeover/lcp2.012.sh
%{_datadir}/ctdb/tests/takeover/lcp2.013.sh
%{_datadir}/ctdb/tests/takeover/lcp2.014.sh
%{_datadir}/ctdb/tests/takeover/lcp2.015.sh
%{_datadir}/ctdb/tests/takeover/lcp2.016.sh
%{_datadir}/ctdb/tests/takeover/lcp2.024.sh
%{_datadir}/ctdb/tests/takeover/lcp2.025.sh
%{_datadir}/ctdb/tests/takeover/lcp2.027.sh
%{_datadir}/ctdb/tests/takeover/lcp2.028.sh
%{_datadir}/ctdb/tests/takeover/lcp2.029.sh
%{_datadir}/ctdb/tests/takeover/lcp2.030.sh
%{_datadir}/ctdb/tests/takeover/lcp2.031.sh
%{_datadir}/ctdb/tests/takeover/lcp2.032.sh
%{_datadir}/ctdb/tests/takeover/lcp2.033.sh
%{_datadir}/ctdb/tests/takeover/lcp2.034.sh
%{_datadir}/ctdb/tests/takeover/lcp2.035.sh
%{_datadir}/ctdb/tests/takeover/nondet.001.sh
%{_datadir}/ctdb/tests/takeover/nondet.002.sh
%{_datadir}/ctdb/tests/takeover/nondet.003.sh

%dir %{_datadir}/ctdb/tests/takeover/scripts
%{_datadir}/ctdb/tests/takeover/scripts/local.sh

%dir %{_datadir}/ctdb/tests/takeover_helper
%{_datadir}/ctdb/tests/takeover_helper/000.sh
%{_datadir}/ctdb/tests/takeover_helper/010.sh
%{_datadir}/ctdb/tests/takeover_helper/011.sh
%{_datadir}/ctdb/tests/takeover_helper/012.sh
%{_datadir}/ctdb/tests/takeover_helper/013.sh
%{_datadir}/ctdb/tests/takeover_helper/014.sh
%{_datadir}/ctdb/tests/takeover_helper/016.sh
%{_datadir}/ctdb/tests/takeover_helper/017.sh
%{_datadir}/ctdb/tests/takeover_helper/018.sh
%{_datadir}/ctdb/tests/takeover_helper/019.sh
%{_datadir}/ctdb/tests/takeover_helper/021.sh
%{_datadir}/ctdb/tests/takeover_helper/022.sh
%{_datadir}/ctdb/tests/takeover_helper/023.sh
%{_datadir}/ctdb/tests/takeover_helper/024.sh
%{_datadir}/ctdb/tests/takeover_helper/025.sh
%{_datadir}/ctdb/tests/takeover_helper/026.sh
%{_datadir}/ctdb/tests/takeover_helper/027.sh
%{_datadir}/ctdb/tests/takeover_helper/028.sh
%{_datadir}/ctdb/tests/takeover_helper/030.sh
%{_datadir}/ctdb/tests/takeover_helper/031.sh
%{_datadir}/ctdb/tests/takeover_helper/110.sh
%{_datadir}/ctdb/tests/takeover_helper/111.sh
%{_datadir}/ctdb/tests/takeover_helper/120.sh
%{_datadir}/ctdb/tests/takeover_helper/121.sh
%{_datadir}/ctdb/tests/takeover_helper/122.sh
%{_datadir}/ctdb/tests/takeover_helper/130.sh
%{_datadir}/ctdb/tests/takeover_helper/131.sh
%{_datadir}/ctdb/tests/takeover_helper/132.sh
%{_datadir}/ctdb/tests/takeover_helper/140.sh
%{_datadir}/ctdb/tests/takeover_helper/150.sh
%{_datadir}/ctdb/tests/takeover_helper/160.sh
%{_datadir}/ctdb/tests/takeover_helper/210.sh
%{_datadir}/ctdb/tests/takeover_helper/211.sh
%{_datadir}/ctdb/tests/takeover_helper/220.sh
%{_datadir}/ctdb/tests/takeover_helper/230.sh
%{_datadir}/ctdb/tests/takeover_helper/240.sh
%{_datadir}/ctdb/tests/takeover_helper/250.sh
%{_datadir}/ctdb/tests/takeover_helper/260.sh

%dir %{_datadir}/ctdb/tests/takeover_helper/scripts
%{_datadir}/ctdb/tests/takeover_helper/scripts/local.sh

%dir %{_datadir}/ctdb/tests/tool
%{_datadir}/ctdb/tests/tool/README
%{_datadir}/ctdb/tests/tool/ctdb.attach.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.attach.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.attach.003.sh
%{_datadir}/ctdb/tests/tool/ctdb.ban.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.ban.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.ban.003.sh
%{_datadir}/ctdb/tests/tool/ctdb.catdb.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.catdb.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.cattdb.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.cattdb.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.continue.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.continue.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.continue.003.sh
%{_datadir}/ctdb/tests/tool/ctdb.deletekey.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.disable.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.disable.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.disable.003.sh
%{_datadir}/ctdb/tests/tool/ctdb.disable.004.sh
%{_datadir}/ctdb/tests/tool/ctdb.enable.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.enable.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.enable.003.sh
%{_datadir}/ctdb/tests/tool/ctdb.getcapabilities.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.getcapabilities.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.getcapabilities.003.sh
%{_datadir}/ctdb/tests/tool/ctdb.getcapabilities.004.sh
%{_datadir}/ctdb/tests/tool/ctdb.getdbmap.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.getdbseqnum.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.getdbseqnum.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.getdbstatus.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.getdbstatus.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.getpid.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.getreclock.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.getreclock.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.getvar.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.getvar.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.ifaces.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.ip.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.ip.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.ip.003.sh
%{_datadir}/ctdb/tests/tool/ctdb.ip.004.sh
%{_datadir}/ctdb/tests/tool/ctdb.ip.005.sh
%{_datadir}/ctdb/tests/tool/ctdb.ip.006.sh
%{_datadir}/ctdb/tests/tool/ctdb.ip.007.sh
%{_datadir}/ctdb/tests/tool/ctdb.ipinfo.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.ipinfo.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.ipinfo.003.sh
%{_datadir}/ctdb/tests/tool/ctdb.listnodes.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.listnodes.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.listvars.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.lvs.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.lvs.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.lvs.003.sh
%{_datadir}/ctdb/tests/tool/ctdb.lvs.004.sh
%{_datadir}/ctdb/tests/tool/ctdb.lvs.005.sh
%{_datadir}/ctdb/tests/tool/ctdb.lvs.006.sh
%{_datadir}/ctdb/tests/tool/ctdb.lvs.007.sh
%{_datadir}/ctdb/tests/tool/ctdb.lvs.008.sh
%{_datadir}/ctdb/tests/tool/ctdb.natgw.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.natgw.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.natgw.003.sh
%{_datadir}/ctdb/tests/tool/ctdb.natgw.004.sh
%{_datadir}/ctdb/tests/tool/ctdb.natgw.005.sh
%{_datadir}/ctdb/tests/tool/ctdb.natgw.006.sh
%{_datadir}/ctdb/tests/tool/ctdb.natgw.007.sh
%{_datadir}/ctdb/tests/tool/ctdb.natgw.008.sh
%{_datadir}/ctdb/tests/tool/ctdb.nodestatus.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.nodestatus.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.nodestatus.003.sh
%{_datadir}/ctdb/tests/tool/ctdb.nodestatus.004.sh
%{_datadir}/ctdb/tests/tool/ctdb.nodestatus.005.sh
%{_datadir}/ctdb/tests/tool/ctdb.nodestatus.006.sh
%{_datadir}/ctdb/tests/tool/ctdb.pdelete.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.ping.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.pnn.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.process-exists.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.process-exists.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.process-exists.003.sh
%{_datadir}/ctdb/tests/tool/ctdb.pstore.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.ptrans.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.readkey.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.recmaster.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.recmaster.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.recover.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.reloadnodes.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.reloadnodes.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.reloadnodes.003.sh
%{_datadir}/ctdb/tests/tool/ctdb.reloadnodes.011.sh
%{_datadir}/ctdb/tests/tool/ctdb.reloadnodes.012.sh
%{_datadir}/ctdb/tests/tool/ctdb.reloadnodes.013.sh
%{_datadir}/ctdb/tests/tool/ctdb.reloadnodes.014.sh
%{_datadir}/ctdb/tests/tool/ctdb.reloadnodes.015.sh
%{_datadir}/ctdb/tests/tool/ctdb.reloadnodes.016.sh
%{_datadir}/ctdb/tests/tool/ctdb.reloadnodes.017.sh
%{_datadir}/ctdb/tests/tool/ctdb.reloadnodes.018.sh
%{_datadir}/ctdb/tests/tool/ctdb.reloadnodes.019.sh
%{_datadir}/ctdb/tests/tool/ctdb.reloadnodes.020.sh
%{_datadir}/ctdb/tests/tool/ctdb.reloadnodes.021.sh
%{_datadir}/ctdb/tests/tool/ctdb.reloadnodes.023.sh
%{_datadir}/ctdb/tests/tool/ctdb.reloadnodes.024.sh
%{_datadir}/ctdb/tests/tool/ctdb.runstate.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.runstate.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.runstate.003.sh
%{_datadir}/ctdb/tests/tool/ctdb.runstate.004.sh
%{_datadir}/ctdb/tests/tool/ctdb.runstate.005.sh
%{_datadir}/ctdb/tests/tool/ctdb.setdbreadonly.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.setdbreadonly.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.setdbreadonly.003.sh
%{_datadir}/ctdb/tests/tool/ctdb.setdbreadonly.004.sh
%{_datadir}/ctdb/tests/tool/ctdb.setdbreadonly.005.sh
%{_datadir}/ctdb/tests/tool/ctdb.setdbsticky.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.setdbsticky.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.setdbsticky.003.sh
%{_datadir}/ctdb/tests/tool/ctdb.setdbsticky.004.sh
%{_datadir}/ctdb/tests/tool/ctdb.setdbsticky.005.sh
%{_datadir}/ctdb/tests/tool/ctdb.setdebug.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.setdebug.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.setdebug.003.sh
%{_datadir}/ctdb/tests/tool/ctdb.setifacelink.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.setifacelink.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.setvar.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.setvar.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.status.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.status.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.stop.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.stop.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.stop.003.sh
%{_datadir}/ctdb/tests/tool/ctdb.unban.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.unban.002.sh
%{_datadir}/ctdb/tests/tool/ctdb.unban.003.sh
%{_datadir}/ctdb/tests/tool/ctdb.uptime.001.sh
%{_datadir}/ctdb/tests/tool/ctdb.writekey.001.sh

%dir %{_datadir}/ctdb/tests/tool/scripts
%{_datadir}/ctdb/tests/tool/scripts/local.sh

%endif

%files help
%{_mandir}/man1/*
%{_mandir}/man3/Parse::Pidl*
%{_mandir}/man5/*
%{_mandir}/man7/*
%exclude %{_mandir}/man7/libsmbclient.7.gz
%{_mandir}/man8/winbindd.8*
%{_mandir}/man8/idmap_*.8*
%{_mandir}/man8/winbind_krb5_localauth.8*
%{_mandir}/man8/winbind_krb5_locator.8*
%{_mandir}/man8/pam_winbind.8*
%{_mandir}/man8/smbspool_krb5_wrapper.8*
%{_mandir}/man8/cifsdd.8.*
%{_mandir}/man8/samba-regedit.8*
%{_mandir}/man8/smbspool.8*
%{_mandir}/man8/eventlogadm.8*
%{_mandir}/man8/smbd.8*
%{_mandir}/man8/nmbd.8*
%{_mandir}/man8/vfs_a*
%{_mandir}/man8/vfs_btrfs.8*
%{_mandir}/man8/vfs_ca*
%{_mandir}/man8/vfs_commit.8*
%{_mandir}/man8/vfs_crossrename.8*
%{_mandir}/man8/vfs_default_quota.8*
%{_mandir}/man8/vfs_dirsort.8*
%{_mandir}/man8/vfs_extd_audit.8*
%{_mandir}/man8/vfs_fake_perms.8*
%{_mandir}/man8/vfs_fileid.8*
%{_mandir}/man8/vfs_fruit.8*
%{_mandir}/man8/vfs_full_audit.8*
%{_mandir}/man8/vfs_gpfs.8*
%{_mandir}/man8/vfs_linux_xfs_sgid.8*
%{_mandir}/man8/vfs_media_harmony.8*
%{_mandir}/man8/vfs_netatalk.8*
%{_mandir}/man8/vfs_nfs4acl_xattr.8*
%{_mandir}/man8/vfs_offline.8*
%{_mandir}/man8/vfs_prealloc.8*
%{_mandir}/man8/vfs_preopen.8*
%{_mandir}/man8/vfs_readahead.8*
%{_mandir}/man8/vfs_readonly.8*
%{_mandir}/man8/vfs_recycle.8*
%{_mandir}/man8/vfs_shadow_copy.8*
%{_mandir}/man8/vfs_shadow_copy2.8*
%{_mandir}/man8/vfs_shell_snap.8*
%{_mandir}/man8/vfs_snapper.8*
%{_mandir}/man8/vfs_streams_depot.8*
%{_mandir}/man8/vfs_streams_xattr.8*
%{_mandir}/man8/vfs_syncops.8*
%{_mandir}/man8/vfs_time_audit.8*
%{_mandir}/man8/vfs_tsmsm.8*
%{_mandir}/man8/vfs_unityed_media.8*
%{_mandir}/man8/vfs_virusfilter.8*
%{_mandir}/man8/vfs_worm.8*
%{_mandir}/man8/vfs_xattr_tdb.8*
%{_mandir}/man8/net.8*
%{_mandir}/man8/pdbedit.8*
%{_mandir}/man8/smbpasswd.8*

%changelog
* Fri Jan 10 2020 openEuler Buildteam <buildteam@openeuler.org> - 4.9.8-9
- clean unused file

* Tue Dec 31 2019 openEuler Buildteam <buildteam@openeuler.org> - 4.9.1-8
- Type:NA
- Id:NA
- SUG:NA
- DESC:update tarball

* Sat Dec 21 2019 openEuler Buildteam <buildteam@openeuler.org> - 4.9.1-7
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:fix CVE

* Thu Dec 19 2019 openEuler Buildteam <buildteam@openeuler.org> - 4.9.1-6
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:modify the changelog message

* Tue Dec 3 2019 openEuler Buildteam <buildteam@openeuler.org> - 4.9.1-5
- Type: NA
- ID:   NA
- SUG:  NA
- DESC: optimize the spec file

* Thu Nov 21 2019 openEuler Buildteam <buildteam@openeuler.org> - 4.9.1-4
- Type: enhancement
- ID:   NA
- SUG:  NA
- DESC:modify spec file 

* Mon Sep 23 2019 huzhiyu<huzhiyu1@huawei.com> - 4.9.1-3
- Package init
