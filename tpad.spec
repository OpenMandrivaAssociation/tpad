Name:		tpad
Summary:	Notepad clone written in Tcl/Tk
Version:	1.3
Release:	%{mkrel 6}
Source0:	http://monitor.deis.unical.it/ant/tpad/%{name}-%{version}.tar.bz2
Patch0:		tpad-1.3.patch
Patch1:		tpad-1.3-use-general-wish.patch
URL:		http://tclpad.sourceforge.net
Group:		Editors
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
License:	GPLv2+
Requires:	tk >= 8.4
Requires:	tcl
# For macros
BuildRequires:	tcl-devel
BuildArch:	noarch

%description
Apart from all the features Notepad has, tpad adds plugins
to invoke some common text utilities without leaving the
editor, an Ascii table, a tip database and support for
regexps. It also is fully configurable.
 
The executable `tpad' is a wish(1) shell script.

%prep  
%setup -q -c %{name}-%{version}
%patch0 -p1 -b .ant
%patch1 -p0 -b .wish

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_datadir}/applications/
cat << EOF > %buildroot%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Exec=%{name}
Icon=editors_section
Categories=TextEditor;
Name=TPad
Comment=Simple clone of Notepad
EOF

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{tcl_sitelib}/tpad%{version}/msgs
install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_datadir}/tpad
install bin/tpad %{buildroot}%{_bindir}/tpad
for libfile in lib/tpad%{version}/*.tcl; do
	install $libfile %{buildroot}%{tcl_sitelib}/tpad%{version};
done
for msgfile in lib/tpad%{version}/msgs/*.msg; do
	install $msgfile %{buildroot}%{tcl_sitelib}/tpad%{version}/msgs;
done
install etc/tpad.conf %{buildroot}%{_sysconfdir}/tpad.conf
install man/man1/tpad.1 %{buildroot}%{_mandir}/man1/tpad.1
for datafile in share/tpad/*; do
	install $datafile %{buildroot}%{_datadir}/tpad;
done

cd %{buildroot}/%{_bindir}
ln -sf tpad tview
cd %{buildroot}/%{_mandir}/man1
ln -sf tpad.1 tview.1

%clean 
rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%{update_menus} 
%endif

%if %mdkversion < 200900
%postun
%{clean_menus} 
%endif

%files
%defattr(-,root,root,0755)
%doc share/doc/tpad/bug.html share/doc/tpad/ChangeLog share/doc/tpad/conf.html share/doc/tpad/embed.html share/doc/tpad/index.html share/doc/tpad/intro.html share/doc/tpad/keys.html share/doc/tpad/log.html share/doc/tpad/mouse.html share/doc/tpad/tidy.html share/doc/tpad/tidy.png share/doc/tpad/todo share/doc/tpad/tpad.html
%{_mandir}/man1/tpad.1*
%{_mandir}/man1/tview.1*
%{_bindir}/tpad
%{_bindir}/tview
%{tcl_sitelib}/tpad%{version}
%{_datadir}/tpad
%{_datadir}/applications/mandriva-%{name}.desktop
%defattr(644,root,root,0755)
%config(noreplace) %{_sysconfdir}/tpad.conf
