import { Link } from 'react-router-dom'
import { Button, Typography } from 'antd'

import logo from '@assets/icons/logo.svg'
import { combineClasses } from '@utils'


export default function Logo({className, color='(--color-dark)'}) {
    return (
        <Link to='/' className='flex'>
            <Button 
                className={combineClasses('p-0!', className)} 
                type='link'
            >
                <img src={logo} />
                <Typography.Text 
                    className={`m-0! font-medium! text-3xl! text-${color}!`}
                >
                    Onest
                </Typography.Text>
            </Button>
        </Link>
    )
}