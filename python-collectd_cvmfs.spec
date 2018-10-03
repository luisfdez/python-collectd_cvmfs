# Created by pyp2rpm-3.3.2
%global pypi_name collectd_cvmfs

Name:           python-%{pypi_name}
Version:        1.0.2
Release:        2%{?dist}
Summary:        Collectd plugin to monitor CvmFS Clients

License:        ASL 2.0
URL:            https://github.com/cvmfs/collectd-cvmfs
Source0:        https://github.com/cvmfs/collectd-cvmfs/archive/%{version}/collectd-cvmfs-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)

BuildRequires:  selinux-policy-devel

%description
Collectd module for CvmFS clients

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}
 
Requires:       python3dist(psutil)
Requires:       python3dist(pyxattr)
Requires:       collectd-python
Requires:       %{name}-selinux = %{version}-%{release}

%description -n python3-%{pypi_name}
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
%py3_build
make -f /usr/share/selinux/devel/Makefile collectd_systemd.pp

%install
%py3_install

mkdir -p %{buildroot}%{_datadir}/selinux/packages/%{name}
install -m 644 -p collectd_cvmfs.pp \
    %{buildroot}%{_datadir}/selinux/packages/%{name}/collectd_cvmfs.pp

%post selinux
/usr/sbin/semodule -i %{_datadir}/selinux/packages/%{name}/collectd_cvmfs.pp >/dev/null 2>&1 || :

%postun selinux
if [ $1 -eq 0 ] ; then
    /usr/sbin/semodule -r collectd_cvmfs >/dev/null 2>&1 || :
fi


%files -n python3-%{pypi_name}
%doc README.rst NEWS.txt
%license LICENSE
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%{_prefix}/share/collectd/%{pypi_name}.db

%files selinux
%{_datadir}/selinux/packages/%{name}/collectd_cvmfs.pp

%changelog
* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri May 25 2018 Steve Traylen <steve.traylen@cern.ch> - 1.0.1-1
- Initial package.
