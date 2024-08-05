import Layout from '@/ui/layouts/authenticated/layout';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Dashboard - Discovery',
  description: ''
};

export default function DashboardLayout({
  children
}: {
  children: React.ReactNode;
}) {
  return <Layout>{children}</Layout>;
}
