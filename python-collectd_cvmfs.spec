# Created by pyp2rpm-3.3.2
%global pypi_name collectd_cvmfs

Name:           python-%{pypi_name}
Version:        1.0.2
Release:        1%{?dist}.1
Summary:        Collectd plugin to monitor CvmFS Clients

License:        ASL 2.0
URL:            https://github.com/cvmfs/collectd-cvmfs
Source0:        https://github.com/cvmfs/collectd-cvmfs/archive/%{version}/collectd-cvmfs-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

BuildRequires:  selinux-policy-devel

%description
Collectd module for CvmFS clients

%package -n     python2-%{pypi_name}
Summary:        %{summary}

Requires:       python-psutil
Requires:       pyxattr
Requires:       collectd

Requires:       %{name}-selinux = %{version}-%{release}

%description -n python2-%{pypi_name}
Collectd module for CvmFS clients

%package selinux
Summary:        selinux policy for collectd cvmfs plugin
Requires:       selinux-policy
Requires:       policycoreutils

%description selinux
This package contains selinux rules to allow the collectd
cvmfs plugin to read fuse file systems.

%prep
%autosetup -n collectd-cvmfs-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%{__python} setup.py build
make -f /usr/share/selinux/devel/Makefile collectd_systemd.pp

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

mkdir -p %{buildroot}%{_datadir}/selinux/packages/%{name}
install -m 644 -p collectd_cvmfs.pp \
    %{buildroot}%{_datadir}/selinux/packages/%{name}/collectd_cvmfs.pp

%post selinux
/usr/sbin/semodule -i %{_datadir}/selinux/packages/%{name}/collectd_cvmfs.pp >/dev/null 2>&1 || :

%postun selinux
if [ $1 -eq 0 ] ; then
    /usr/sbin/semodule -r collectd_cvmfs >/dev/null 2>&1 || :
fi

%files -n python2-%{pypi_name}
%doc README.rst NEWS.txt LICENSE
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%{_prefix}/share/collectd/%{pypi_name}.db

%files selinux
%{_datadir}/selinux/packages/%{name}/collectd_cvmfs.pp

%changelog
* Wed May 30 2018 Steve Traylen <steve.traylen@cern.ch> - 1.0.1-1 1
- Backport to el6

* Fri May 25 2018 Steve Traylen <steve.traylen@cern.ch> - 1.0.1-1
- Initial package.
