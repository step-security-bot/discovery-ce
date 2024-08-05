import { Icons } from '@discovery/shared/components';

export type NavItem = {
  title: string;
  href: string;
  disabled?: boolean;
  icon: keyof typeof Icons;
};
