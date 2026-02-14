import { 
   PlusCircleOutlined, 
   UnorderedListOutlined,
   HeartOutlined,
   MessageOutlined,
   LogoutOutlined,
   SettingOutlined
} from "@ant-design/icons"


export const PROFILE_LAYOUT_LINKS = [
    {
       text: 'My listings',
       href: '/profile/my_listings',
       icon: (
        <UnorderedListOutlined />
       ) 
    },
    {
       text: 'Post a Listing',
       href: '/profile/post_listing',
       icon: (
        <PlusCircleOutlined />
       ) 
    },
    {
       text: 'Favorite',
       href: '/profile/favorite',
       icon: (
         <HeartOutlined />
       ) 
    },
    {
       text: 'Chats',
       href: '/profile/chats',
       icon: (
         <MessageOutlined />
       ) 
    },
    {
       text: 'Settings',
       href: '/profile/settings',
       icon: (
        <SettingOutlined />
       ) 
    },
    {
       text: 'Sign Out',
       href: '/auth/signout',
       icon: (
        <LogoutOutlined />
       ) 
    }
]