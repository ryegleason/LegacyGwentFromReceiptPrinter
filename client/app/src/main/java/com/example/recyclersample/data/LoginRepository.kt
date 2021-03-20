package com.example.recyclersample.data

import com.example.recyclersample.data.model.ConnectionInfo

/**
 * Class that requests authentication and user information from the remote data source and
 * maintains an in-memory cache of login status and user credentials information.
 */

class LoginRepository(val dataSource: LoginDataSource) {

    // in-memory cache of the loggedInUser object
    var user: ConnectionInfo? = null
        private set

    val isLoggedIn: Boolean
        get() = user != null

    init {
        // If user credentials will be cached in local storage, it is recommended it be encrypted
        // @see https://developer.android.com/training/articles/keystore
        user = null
    }

    fun logout(connectionInfo: ConnectionInfo) {
        user = null
        dataSource.logout(connectionInfo)
    }

    fun login(ip: String, port: String): Result<ConnectionInfo> {
        // handle login
        val result = dataSource.login(ip, port)

        if (result is Result.Success) {
            setLoggedInUser(result.data)
        }

        return result
    }

    private fun setLoggedInUser(connectionInfo: ConnectionInfo) {
        this.user = connectionInfo
        // If user credentials will be cached in local storage, it is recommended it be encrypted
        // @see https://developer.android.com/training/articles/keystore
    }
}