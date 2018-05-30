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
BuildRequires:  python2-setuptools

%description
Collectd module for CvmFS clients

%package -n     python2-%{pypi_name}
Summary:        %{summary}
 
Requires:       python2-psutil
Requires:       pyxattr
Requires:       collectd
%description -n python2-%{pypi_name}
Collectd module for CvmFS clients


%prep
%autosetup -n collectd-cvmfs-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py2_build

%install
%py2_install

%files -n python2-%{pypi_name}
%doc README.rst NEWS.txt
%license LICENSE
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%{_prefix}/share/collectd/%{pypi_name}.db

%changelog
* Wed May 30 2018 Steve Traylen <steve.traylen@cern.ch> - 1.0.1-1 1
- Backport to epel7

* Fri May 25 2018 Steve Traylen <steve.traylen@cern.ch> - 1.0.1-1
- Initial package.
