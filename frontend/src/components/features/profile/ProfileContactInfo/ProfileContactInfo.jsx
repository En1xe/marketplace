export default function ProfileContactInfo({email, address}) {
    return (
        <div className="flex flex-col gap-4">
            <ul>
                <li className='flex gap-3 text-(--color-dark-700)'>
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M21 5.25L12 13.5L3 5.25" stroke="#00AAFF" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
                        <path d="M3 5.25H21V18C21 18.1989 20.921 18.3897 20.7803 18.5303C20.6397 18.671 20.4489 18.75 20.25 18.75H3.75C3.55109 18.75 3.36032 18.671 3.21967 18.5303C3.07902 18.3897 3 18.1989 3 18V5.25Z" stroke="#00AAFF" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
                        <path d="M10.3636 12L3.2312 18.538" stroke="#00AAFF" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
                        <path d="M20.7687 18.5381L13.6362 12" stroke="#00AAFF" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                    {email}
                </li>
                <li className='flex gap-3 text-(--color-dark-700)'>
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M5.25 21.75H18.75" stroke="#00AAFF" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
                        <path d="M12 12.75C13.6569 12.75 15 11.4069 15 9.75C15 8.09315 13.6569 6.75 12 6.75C10.3431 6.75 9 8.09315 9 9.75C9 11.4069 10.3431 12.75 12 12.75Z" stroke="#00AAFF" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
                        <path d="M19.5 9.75C19.5 16.5 12 21.75 12 21.75C12 21.75 4.5 16.5 4.5 9.75C4.5 7.76088 5.29018 5.85322 6.6967 4.4467C8.10322 3.04018 10.0109 2.25 12 2.25C13.9891 2.25 15.8968 3.04018 17.3033 4.4467C18.7098 5.85322 19.5 7.76088 19.5 9.75V9.75Z" stroke="#00AAFF" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                    {address}
                </li>
            </ul>
        </div>
    )
}