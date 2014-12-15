Name:	    x11-common
Summary:    Configuration-files needed by xserver for autorun
Version:    0.0.1
Release:    1
BuildArch:  noarch
Group:      Graphics & UI Framework/X Window System
License:    MIT
Source:    %{name}-%{version}.tar.gz

Requires:   xorg-server
Requires:   xorg-launch-helper
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

mkdir -p %{buildroot}%{_unitdir}
mv  %{buildroot}/display-manager.path %{buildroot}%{_unitdir}
mv  %{buildroot}/display-manager.service %{buildroot}%{_unitdir}
mv  %{buildroot}/display-manager-run.service %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_unitdir}/multi-user.target.wants
ln -sf ../display-manager.service %{buildroot}%{_unitdir}/multi-user.target.wants/display-manager.service
ln -sf ../display-manager-run.service %{buildroot}%{_unitdir}/multi-user.target.wants/display-manager-run.service

# rules for /dev/input devices
mkdir -p %{buildroot}%{_sysconfdir}/udev/rules.d/
cat >%{buildroot}%{_sysconfdir}/udev/rules.d/99-input.rules <<'EOF'
SUBSYSTEM=="input", MODE="0660", GROUP="input", SECLABEL{smack}="^"
EOF

%pre
# create group 'input' if needed
getent group input >/dev/null || %{_sbindir}/groupadd -r -o input

%files
%defattr(-,root,root,-)
%{_unitdir}/display-manager.path
%{_unitdir}/display-manager.service
%{_unitdir}/display-manager-run.service
%{_unitdir}/multi-user.target.wants/display-manager.service
%{_unitdir}/multi-user.target.wants/display-manager-run.service
%config %{_sysconfdir}/udev/rules.d/*

