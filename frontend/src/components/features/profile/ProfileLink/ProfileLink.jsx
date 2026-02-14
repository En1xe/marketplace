import { Link } from 'react-router-dom';


export default function ProfileLink({className, is_active, to, children, ...props}) {
    return (
        <Link 
            to={to} 
            className={`
            w-full! py-3! px-6! flex! text-[18px]! hover:text-(--color-accent)!
            ${is_active 
                ? 'bg-(--color-primary-50)! border-l-2 border-l-(--color-accent) \
                    text-(--color-accent)! pointer-events-none' 
                : 'text-(--color-grey-500)!'}
            `}
        >
            {children}
        </Link>
    )
}