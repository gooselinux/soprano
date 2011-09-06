
# fedora review: http://bugzilla.redhat.com/248120

# set this to 0 to disable -apidocs for a faster build
%define apidocs 1 

Summary: Qt wrapper API to different RDF storage solutions
Name:    soprano
Version: 2.3.1
Release: 1.2%{?dist}

Group:   System Environment/Libraries
License: LGPLv2+
URL:     http://sourceforge.net/projects/soprano
Source0: http://downloads.sf.net/soprano/soprano-%{version}.tar.bz2
Source1: soprano-svn_checkout.sh 
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: clucene-core-devel >= 0.9.20-2
BuildRequires: cmake
BuildRequires: kde-filesystem
# for backends/virtuoso
#BuildRequires: libiodbc-devel
BuildRequires: qt4-devel
BuildRequires: redland-devel >= 1.0.6
BuildRequires: raptor-devel >= 1.4.15

%if "%{?apidocs}" == "1"
BuildRequires: doxygen
BuildRequires: graphviz
BuildRequires: qt4-doc
%endif

%description
%{summary}.

%package devel
Summary: Developer files for %{name}
Group:   Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: qt4-devel
Requires: pkgconfig
%description devel
%{summary}.

%package apidocs
Group: Development/Documentation
Summary: Soprano API documentation
Requires: %{name} = %{version}
%if 0%{?fedora} > 9 || 0%{?rhel} >= 6
# help workaround yum bug http://bugzilla.redhat.com/502401
Obsoletes: soprano-apidocs < 2.2.3-2 
BuildArch: noarch
%endif

%description apidocs
This package includes the Soprano API documentation in HTML
format for easy browsing.


%prep
%setup -q -n soprano-%{version}


%build

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} \
  -DDATA_INSTALL_DIR:PATH=%{_kde4_appsdir} \
  -DQT_DOC_DIR=`pkg-config --variable=docdir Qt` \
  -DSOPRANO_BUILD_API_DOCS:BOOL=%{?apidocs} \
  .. 
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf $RPM_BUILD_ROOT

make install/fast DESTDIR=$RPM_BUILD_ROOT -C %{_target_platform}


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING* README TODO
%{_bindir}/sopranocmd
%{_bindir}/sopranod
%{_bindir}/onto2vocabularyclass
%{_libdir}/libsoprano.so.4*
%{_libdir}/libsopranoclient.so.1*
%{_libdir}/libsopranoindex.so.1*
%{_libdir}/libsopranoserver.so.1*
%{_libdir}/soprano/
%{_datadir}/soprano/
%{_datadir}/dbus-1/interfaces/org.soprano.*.xml

%files devel
%defattr(-,root,root,-)
%{_datadir}/soprano/cmake/
%{_libdir}/libsoprano*.so
%{_libdir}/pkgconfig/soprano.pc
%{_includedir}/soprano/
%{_includedir}/Soprano/

%if "%{?apidocs}" == "1"
%files apidocs
%defattr(-,root,root,-)
%doc %{_target_platform}/docs/html
%endif


%changelog
* Tue Dec 08 2009 Dennis Gregorovic <dgregor@redhat.com> - 2.3.1-1.2
- Rebuilt for RHEL 6

* Fri Nov 13 2009 Dennis Gregorovic <dgregor@redhat.com> - 2.3.1-1.1
- Fix conditional for RHEL

* Mon Sep 14 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.3.1-1
- soprano-2.3.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 16 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.3.0-1
- soprano-2.3.0
- upstream dropped virtuoso backend  ):

* Fri Jun 26 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.2.69-1
- soprano-2.2.69

* Tue Jun 09 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.2.67-2
- upstream soprano-2.2.67 tarball

* Wed Jun 03 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.2.67-1
- soprano-2.2.67, 20090603 snapshot from kdesupport 

* Wed May  6 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.2.3-2
- %%files: drop ownership of %%_datadir/dbus-1.0/interfaces (#334681)
- %%files: track shlib sonames
- make -apidocs noarch

* Mon Mar  2 2009 Lukáš Tinkl <ltinkl@redhat.com> - 2.2.3-1
- update to 2.2.3, fix apidox building

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 29 2009 Lukáš Tinkl <ltinkl@redhat.com> 2.2.1-1
- update to 2.2.1

* Tue Jan 27 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.2-1
- update to 2.2

* Fri Jan 09 2009 Than Ngo <than@redhat.com> - 2.1.64-1
- update to 2.1.64 (2.2 beta 1)

* Sun Sep 28 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.1.1-1
- update to 2.1.1

* Tue Jul 22 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.1-1
- update to 2.1
- BR graphviz for apidocs

* Fri Jul 11 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.0.99-1
- update to 2.0.99 (2.1 RC 1)

* Thu May 1 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.0.98-1
- update to 2.0.98 (2.1 alpha 1)

* Thu Mar 6 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.0.3-2
- build apidocs and put them into an -apidocs subpackage (can be turned off)
- BR doxygen and qt4-doc when building apidocs

* Tue Mar 4 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.0.3-1
- update to 2.0.3 (bugfix release)

* Fri Feb 22 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.0.2-1
- update to 2.0.2 (bugfix release)
- drop glibc/open (missing mode) patch (fixed upstream)

* Sat Feb 9 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.0.0-2
- rebuild for GCC 4.3

* Mon Jan 07 2008 Than Ngo <than@redhat.com> 2.0.0-1
- 2.0.0

* Sun Dec 2 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 1.98.0-1
- soprano-1.98.0 (soprano 2 rc 1)
- update glibc/open patch

* Sat Nov 10 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.97.1-2
- glibc/open patch

* Sat Nov 10 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.97.1-1
- soprano-1.97.1 (soprano 2 beta 4)

* Fri Oct 26 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 1.95.0-3
- BR clucene-core-devel >= 0.9.20-2 to make sure we get a fixed package

* Fri Oct 26 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 1.95.0-2
- drop findclucene patch, fixed in clucene-0.9.20-2

* Tue Oct 16 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 1.95.0-1
- update to 1.95.0 (Soprano 2 beta 2)
- new BRs clucene-core-devel, raptor-devel >= 1.4.15
- now need redland-devel >= 1.0.6
- add patch to find CLucene (clucene-config.h is moved in the Fedora package)
- new Requires: pkg-config for -devel

* Wed Aug 22 2007 Rex Dieter <rdietr[AT]fedoraproject.org> 0.9.0-4
- respin (BuildID)

* Fri Aug 3 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.9.0-3
- specify LGPL version in License tag

* Sun Jul 15 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.9.0-2
- BR: cmake (doh)

* Wed Jun 27 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.9.0-1
- soprano-0.9.0
- first try

