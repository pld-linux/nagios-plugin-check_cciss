%define		plugin	check_cciss
Summary:	Nagios plugin to check the status of HP Smart Array Hardware
Name:		nagios-plugin-%{plugin}
# revision from download page
Version:	1.11
Release:	1
License:	GPL
Group:		Networking
# http://exchange.nagios.org/components/com_mtree/attachment.php?link_id=671&cf_id=35
Source0:	check_cciss
URL:		http://exchange.nagios.org/directory/Plugins/Hardware/Storage-Systems/RAID-Controllers/check_cciss--2D-HP-and-Compaq-Smart-Array-Hardware-status/details
# non-free, http://downloads.linux.hp.com/SDR/downloads/proliantsupportpack/
Requires:	hpacucli
Requires:	nagios-core
Requires:	nagios-plugins-libs
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		plugindir	%{_prefix}/lib/nagios/plugins
%define		_sysconfdir	/etc/nagios/plugins

%description
This plugin checks hardware status for Smart Array Controllers,
using the HP Array Configuration Utility CLI. (Array, controller,
cache, disk, battery, etc...).

%prep
%setup -qcT

install %{SOURCE0} %{plugin}

cat > nagios.cfg <<'EOF'
# Usage:
# %{plugin}
define command {
	command_name    %{plugin}
	command_line    %{plugindir}/%{plugin}
}

define service {
	use                     generic-service
	name                    cciss
	service_description     cciss
	register                0

	normal_check_interval   15
	notification_interval   300
	check_command           check_cciss
}

define service {
	use                     generic-service
	name                    hpsa
	service_description     hpsa
	register                0

	normal_check_interval   15
	notification_interval   300
	check_command           check_cciss -s
}
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{plugindir}}

install %{plugin} $RPM_BUILD_ROOT%{plugindir}/%{plugin}
cp -a nagios.cfg $RPM_BUILD_ROOT%{_sysconfdir}/%{plugin}.cfg

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{plugin}.cfg
%attr(755,root,root) %{plugindir}/%{plugin}
