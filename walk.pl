#!/usr/bin/env perl

use warnings;
use strict;
use 5.010;

use File::Next;

my $start = shift or die 'Specify a directory to walk';

my $iter = File::Next::files(
    {
        descend_filter => sub { $_ ne '.git' },
        sort_files     => 1,
    },
    $start
);

my %seen;
while ( my $file = $iter->() ) {
    #    ++$seen{$file};
    say $file;
}
