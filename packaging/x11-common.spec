Name:	    x11-common
Summary:    Configuration-files needed by xserver for autorun
Version:    0.0.1
Release:    1
BuildArch:  noarch
Group:      Graphics & UI Framework/X Window System
License:    MIT
Source:    %{name}-%{version}.tar.gz

Requires:   xorg-server
Conflicts:  weston-common

%description
Description: %{summary}


%prep
%setup -q

%build
%reconfigure \
	--with-arch=noarch \
	--with-conf-prefix=/

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

mkdir -p %{buildroot}/usr/lib/systemd/system
mv  %{buildroot}/display-manager.path %{buildroot}/usr/lib/systemd/system/
mv  %{buildroot}/display-manager.service %{buildroot}/usr/lib/systemd/system/
mv  %{buildroot}/display-manager-run.service %{buildroot}/usr/lib/systemd/system/
mkdir -p %{buildroot}/usr/lib/systemd/system/multi-user.target.wants
ln -sf ../display-manager.service %{buildroot}/usr/lib/systemd/system/multi-user.target.wants/display-manager.service
ln -sf ../display-manager-run.service %{buildroot}/usr/lib/systemd/system/multi-user.target.wants/display-manager-run.service

%files
%defattr(-,root,root,-)
/usr/lib/systemd/system/display-manager.path
/usr/lib/systemd/system/display-manager.service
/usr/lib/systemd/system/display-manager-run.service
/usr/lib/systemd/system/multi-user.target.wants/display-manager.service
/usr/lib/systemd/system/multi-user.target.wants/display-manager-run.service
