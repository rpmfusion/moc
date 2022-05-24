## Debug builds?
%bcond_with debug
#

# MOC is not ready for FFMpeg-5+ yet
%if 0%{?fedora} > 34
%bcond_with oldffmpeg
%else
%bcond_with oldffmpeg
%endif

# Filtering of private libraries
%global __provides_exclude_from ^%{_libdir}/mocp/.*\\.so$
#

%global checkout 3005

# Set up a new macro to define MOC's 'mocp' executable
%global   exec   mocp

Name:    moc
Summary: Music on Console - Console audio player for Linux/UNIX
Version: 2.6
Release: 0.45.svn%{checkout}%{?dist}
License: GPLv3+
URL:     http://moc.daper.net

## Source archive made by using following commands
## svn co svn://svn.daper.net/moc/trunk
## rm -rf trunk/.svn
## tar -cvzf moc-svn%%{checkout}.tar.gz trunk
Source0: moc-svn%{checkout}.tar.gz
Patch0:  %{name}-r2961+lt_init-1.patch

# RHBZ #1963427
Patch1:  %{name}-change_private_libdir.patch

# Initial fix for FFMpeg-5 
Patch2:  %{name}-bugfix-ffmpeg5.patch

BuildRequires: pkgconfig(ncurses)
BuildRequires: pkgconfig(alsa) 
BuildRequires: pkgconfig(jack)
BuildRequires: pkgconfig(libcurl) 
BuildRequires: pkgconfig(samplerate) 
BuildRequires: pkgconfig(taglib) 
BuildRequires: pkgconfig(speex) 
BuildRequires: pkgconfig(id3tag) 
BuildRequires: pkgconfig(vorbis) 
BuildRequires: pkgconfig(flac) 
BuildRequires: pkgconfig(zlib) 
BuildRequires: pkgconfig(sndfile) 
BuildRequires: pkgconfig(libmodplug) 
BuildRequires: pkgconfig(libtimidity) 
BuildRequires: pkgconfig(wavpack) 
BuildRequires: libdb-devel 
BuildRequires: libtool-ltdl-devel 
BuildRequires: gettext-devel 
BuildRequires: pkgconfig(opus)
BuildRequires: libtool
#BuildRequires: librcc-devel
BuildRequires: popt-devel
%if %{with oldffmpeg}
BuildRequires: compat-ffmpeg4-devel
%else
BuildRequires: ffmpeg-devel
%endif
BuildRequires: libmad-devel
BuildRequires: faad2-devel

BuildRequires: autoconf, automake
BuildRequires: gcc
BuildRequires: make
BuildRequires: patchelf

%description
MOC (music on console) is a console audio player for LINUX/UNIX designed to be
powerful and easy to use. You just need to select a file from some directory
using the menu similar to Midnight Commander, and MOC will start playing all
files in this directory beginning from the chosen file.

%prep
%autosetup -N -n trunk

%patch0 -p1
%patch1 -p1
%if %{without oldffmpeg}
%patch2 -p1
%endif

%build
mv configure.in configure.ac
libtoolize -ivfc
autoreconf -ivf

%if %{with debug}
export CFLAGS="-O0 -g"
%endif
export LT_SYS_LIBRARY_PATH=%{_libdir}/mocp
%configure LT_SYS_LIBRARY_PATH=%{_libdir}/mocp \
 --disable-static --disable-silent-rules --enable-rpath --without-rcc \
 --with-oss --with-alsa --with-jack --with-aac --with-mp3 \
 --with-musepack --with-vorbis --with-flac --with-wavpack \
 --with-sndfile --with-modplug --with-speex \
 --with-samplerate --with-curl --without-magic \
%if %{with oldffmpeg}
 ffmpeg_CPPFLAGS=-I%{_includedir}/compat-ffmpeg28 \
 ffmpeg_CFLAGS=-I%{_includedir}/compat-ffmpeg28 \
 ffmpeg_LIBS="-L%{_libdir}/compat-ffmpeg4 -lswscale -lavcodec -lavdevice -lavfilter -lavresample -lpostproc -lavutil" \
%else
 --with-ffmpeg \
%endif
%if %{with debug}
 --enable-debug \
%else
 --disable-debug \
%endif
 CPPFLAGS="-I%{_includedir}/libdb -fPIC"
 
%make_build

%install
%make_install
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/mocp/decoder_plugins/*.la

patchelf --set-rpath %{_libdir}/mocp/decoder_plugins %{buildroot}%{_bindir}/*

%files
%doc README README_equalizer AUTHORS ChangeLog config.example keymap.example NEWS
%license COPYING
%{_bindir}/%{exec}
%{_datadir}/%{name}/
%{_mandir}/man1/%{exec}.*
%dir %{_libdir}/mocp
%dir %{_libdir}/mocp/decoder_plugins
%{_libdir}/mocp/decoder_plugins/*.so

%changelog
* Tue May 24 2022 Antonio Trande <sagitter@fedoraproject.org> - 2.6-0.45.svn3005
- Rebuild for RPMFusion bug #6310
- Disable RCC support

* Thu Feb 10 2022 Antonio Trande <sagitter@fedoraproject.org> - 2.6-0.44.svn3005
- Bugfix for building against ffmpeg 5+

* Fri Nov 12 2021 Leigh Scott <leigh123linux@gmail.com> - 2.6-0.43.svn3005
- Rebuilt for new ffmpeg snapshot

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.6-0.42.svn3005
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Jul 04 2021 Antonio Trande <sagitter@fedoraproject.org> - 2.6-0.41.svn3005
- Disable debug mode

* Sat Jul 03 2021 Antonio Trande <sagitter@fedoraproject.org> - 2.6-0.40.svn3005
- Restore rpath to the private decoder directory

* Sat Jul 03 2021 Antonio Trande <sagitter@fedoraproject.org> - 2.6-0.39.svn3005
- Enable RCC support

* Sun May 23 2021 Antonio Trande <sagitter@fedoraproject.org> - 2.6-0.38.svn3005
- Fix conflicts of %%{_libdir}/%%{name}
- Temporary disable RCC support (rhbz#1963427)

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.6-0.37.svn3005
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 31 2020 Antonio Trande <sagitter@fedoraproject.org> - 2.6-0.36.svn3005
- Add make BR

* Tue Aug 18 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.6-0.35.svn3005
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Feb 22 2020 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 2.6-0.34.svn3005
- Rebuild for ffmpeg-4.3 git

* Wed Feb 19 2020 Antonio Trande <sagitter@fedoraproject.org> - 2.6-0.33.svn3005
- SVN checkout svn3005

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.6-0.32.svn2992
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Aug 07 2019 Leigh Scott <leigh123linux@gmail.com> - 2.6-0.31.svn2992
- Rebuild for new ffmpeg version

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.6-0.30.svn2992
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Dec 27 2018 Antonio Trande <sagitter@fedoraproject.org> - 2.6-0.29.svn2992
- SVN checkout svn2992

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.6-0.28.alpha3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Apr 24 2018 Antonio Trande <sagitter@fedoraproject.org> - 2.6-0.27.alpha3
- Remove unused ffmpeg dependency

* Sun Apr 22 2018 Antonio Trande <sagitter@fedoraproject.org> - 2.6-0.26.alpha3
- Use %%{?_isa} on 'Requires' package

* Thu Mar 08 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 2.6-0.25.alpha3
- Rebuilt for new ffmpeg snapshot

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 2.6-0.24.alpha3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 19 2018 Antonio Trande <sagitter@fedoraproject.org> - 2.6-0.23.alpha3
- Rename patch for ffmpeg-3.5 and applied on fedora 28+
- Add patch for timidity from upstream

* Thu Jan 18 2018 Leigh Scott <leigh123linux@googlemail.com> - 2.6-0.22.alpha3
- Rebuilt for ffmpeg-3.5 git

* Thu Dec 07 2017 Antonio Trande <sagitter@fedoraproject.org> - 2.6-0.21.alpha3
- Use GPLv3+ license only

* Tue Oct 17 2017 Leigh Scott <leigh123linux@googlemail.com> - 2.6-0.20.alpha3
- Rebuild for ffmpeg update

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 2.6-0.19.alpha3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Apr 29 2017 Leigh Scott <leigh123linux@googlemail.com> - 2.6-0.18.alpha3
- Rebuild for ffmpeg update

* Mon Mar 20 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 2.6-0.17.alpha3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Feb 13 2017 Antonio Trande <sagitter@fedoraproject.org> - 2.6-0.16.alpha3
- Rebuild for GCC 7

* Wed Nov 16 2016 Antonio Trande <sagitter@fedoraproject.org> - 2.6-0.15.alpha3
- Update to alpha3

* Sun Nov 06 2016 Leigh Scott <leigh123linux@googlemail.com> - 2.6-0.14.alpha2
- rebuild for libtimidity .so bump

* Fri Aug 12 2016 Antonio Trande <sagitter@fedoraproject.org> - 2.6-0.13.alpha2
- Filtering of private libraries

* Sat Jul 30 2016 Julian Sikorski <belegdol@fedoraproject.org> - 2.6-0.12.alpha2
- Rebuilt for ffmpeg-3.1.1

* Thu Jul 07 2016 Antonio Trande <sagitter@fedoraproject.org> - 2.6-0.11.alpha2
- Add ffmpeg as Requires package

* Sun Jun 05 2016 Antonio Trande <sagitter@fedoraproject.org> - 2.6-0.10.alpha2
- Update to commit 2880
- Rebuild for ffmpeg 2.8.7

* Mon May 16 2016 Antonio Trande <sagitter@fedoraproject.org> - 2.6-0.9.alpha2
- Fix faad2 dependencies

* Mon Apr 25 2016 Antonio Trande <sagitter@fedoraproject.org> - 2.6-0.8.alpha2
- ldconfig commands removed

* Thu Jan 28 2016 Antonio Trande <sagitter@fedoraproject.org> - 2.6-0.7.alpha2
- Force -fstack-protector-all
- Tries upstream patch

* Sun Nov 01 2015 Antonio Trande <sagitter@fedoraproject.org> - 2.6-0.6.alpha1
- Hardened builds on <F23

* Tue Sep 29 2015 Antonio Trande <sagitter@fedoraproject.org> - 2.6-0.5.alpha1
- Update to svn commit #2776
- Used %%license macro

* Tue Mar 24 2015 Antonio Trande <sagitter@fedoraproject.org> - 2.6-0.4.alpha1
- Update to svn commit #2770

* Mon Oct 20 2014 Sérgio Basto <sergio@serjux.com> - 2.6-0.3.alpha1
- Rebuilt for FFmpeg 2.4.3

* Fri Sep 26 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.6-0.2.alpha1
- Rebuilt for FFmpeg 2.4.x

* Tue Sep 02 2014 Antonio Trande <sagitter@fedoraproject.org> 2.6-0.1.alpha1
- Leap to 2.6-alpha1 release

* Tue Sep 02 2014 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-2
- Spec cleanups

* Sat Aug 30 2014 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-1
- Update to release 2.5.0 (Consolidation)

* Thu Aug 07 2014 Sérgio Basto <sergio@serjux.com> - 2.5.0-0.16.beta2
- Rebuilt for ffmpeg-2.3
- Conditional builds for ARM

* Tue May 13 2014 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.15.beta2
- New svn commit of MOC-2.5.0 pre-release (r2641)

* Sat Mar 29 2014 Sérgio Basto <sergio@serjux.com> 2.5.0-0.14.beta2
- Rebuilt for ffmpeg-2.2

* Thu Mar 20 2014 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.13.beta2
- New svn commit of MOC-2.5.0 pre-release
- Fixed release increment number for the pre-releases

* Wed Feb 26 2014 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.12.beta2
- Fix unstripped-binary-or-object warnings for ARM builds

* Wed Feb 05 2014 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.11.beta2
- Update to 2.5.0-beta2
- Removed previous patches

* Tue Jun 18 2013 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.10.beta1
- Added patchset to fix "Unsupported sample size!" error
  See http://moc.daper.net/node/862 for more details
- Added patch for 'sizeof' argument bug
- Added BR: Autoconf and Automake-1.13 (temporarily)
- 'configure.in' renaming

* Sat Jun 08 2013 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.9.beta1
- Removed some explicit Requires (curl, jack-audio-connection-kit, ncurses, speex)

* Fri Jun 07 2013 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.8.beta1
- Fixed Source0 line
- Package owns %%{_libdir}/%%{name} directory

* Mon May 20 2013 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.7.beta1
- Dist tag changed to %%{?dist}

* Tue Apr 09 2013 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.6.beta1
- Removed autoreconf task from %%build section

* Fri Apr 05 2013 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.5.beta1
- Removed libRCC explicit require

* Sun Mar 03 2013 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.4.beta1
- Removed DESTDIR from %%make_install
- Changed source link with a public one
- Set up a new macro to define MOC's 'mocp' executable
- Added %%{name} prefix to the patch

* Tue Dec 25 2012 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.3.beta1
- Added librcc support (fixes encoding in broken mp3 tags)

* Mon Oct 22 2012 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.2.beta1
- Added patch to fix FSF address

* Mon Oct 22 2012 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.1.beta1
- 2.5.0-beta1
